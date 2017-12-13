import os


POSTGRES = {
    'user': 'ivan2',
    'pw': '1234',
    'db': 'shopping_list',
    'host': 'localhost',
    'port': '5432',
}
TEST_POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'tests',
    'host': 'localhost',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % TEST_POSTGRES
SQLALCHEMY_DATABASE_URI2 = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

SECRET_KEY='this-is-my-secret-key'
