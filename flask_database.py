import atexit

from DBUtils.PooledDB import PooledDB, SharedDBConnection
from flask import current_app, g


class Database:
    def __init__(self, app=None, db_module=None, **db_args):
        self.pool = None
        self.storage = self
        self.is_detached = False
        if app or db_module:
            self.init_app(app, db_module, **db_args)

    def init_app(self, app, db_module, **db_args):
        self.pool = PooledDB(
            db_module,
            **db_args
        )
        if app:
            self.storage = g
            app.teardown_appcontext(self._teardown)
    
    def fetch_one(self, sql, args=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, sql, args=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def run(self, sql, args=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, args)
        last_id = cursor.lastrowid
        self.conn.commit()
        cursor.close()
        return last_id
    
    def __enter__(self):
        self.storage.dbcursor = self.conn.cursor()
        return self.storage.dbcursor
    
    def __exit__(self, exc, exc_val, exc_tb):
        if exc:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.storage.dbcursor.close()
        del self.storage.dbcursor

    @property
    def conn(self):
        try:
            return self.storage.dbconn
        except AttributeError:
            self.storage.dbconn = self.pool.connection()
        return self.storage.dbconn
    
    def detach(self):
        """Separates from Flask (ie. if using database in a script)"""
        if not self.is_detached:
            self.is_detached = True
            self.storage = self
            atexit.register(lambda: self._teardown(None))

    def _teardown(self, exception):
        if hasattr(self.storage, 'dbconn'):
            self.storage.dbconn.close()
            del self.storage.dbconn
