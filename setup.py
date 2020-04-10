from setuptools import setup

setup(
    name='flask-database',
    version='0.1.3',
    description='Simple Flask database integration',
    url='https://github.com/matthewscholefield/flask-database',
    author='Matthew D. Scholefield',
    author_email='matthew331199@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='flask database',
    py_modules=['flask_database'],
    install_requires=[
        'Flask',
        'DBUtils'
    ],
)
