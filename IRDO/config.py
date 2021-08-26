from logging import debug
from os import environ
from re import DEBUG

class Config(object):
    SQLALCHEMY_DATABASE_URI = environ.get(
        # 'IRDO_DATABASE_URL', 'sqlite:///database.sqlite3?check_same_thread=False'
        'IRDO_DATABASE_URL', 'mysql://root:P@55w0rd.@localhost/api'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_SERVER = '127.0.0.1'

class DebugConfig(Config):
    DEBUG = True
    SECRET_KEY = environ.get(
        'IRDO_SECRET_KEY', 'dont rely on my key'
    )

class ProductionConfig(Config):
    DEBUG = False
    DB_SERVER = '192.168.0.208'
    SECRET_KEY = environ.get('IRDO_SECRET_KEY')
    VAULT_ADDR = environ.get('VAULT_ADDR')
    VAULT_TOKEN = environ.get('VAULT_TOKEN')

class TestConfig(Config):
    DB_SERVER = '127.0.0.1'
    DEBUG = True
    SECRET_KEY = 'thiskey'
    TESTING = True 
    SQLALCHEMY_DATABASE_URI  ='sqlite:///:memory:'

app_config_dict = {
    'ProductionConfig' : ProductionConfig,
    'Debug' : DebugConfig,
    'Testing' : TestConfig,
}
