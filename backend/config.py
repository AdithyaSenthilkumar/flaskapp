from decouple import config
from datetime import timedelta
import os

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

#Global Configurations
class Config:
    SECRET_KEY=config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS',cast=bool)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)

#Development Configurations -> inherit from global configurations
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'invoices_dev.db') #sqlite database
    DEBUG=True  #flask will reload itself everytime a change is made to the code
    SQLALCHEMY_ECHO=True  #can see generated sql queries in terminal everytime a query is executed


#Production Configurations -> inherit from global configurations
class ProdConfig(Config):
    
    pass


#Testing Configurations -> inherit from global configurations
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(BASE_DIR,'invoices_test.db') #sqlite database
    TESTING=True
    
    pass

config_dict={
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}