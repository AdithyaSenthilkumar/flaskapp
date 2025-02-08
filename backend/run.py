from main import create_app
from config import config_dict,DevConfig,ProdConfig,TestConfig 

if __name__ == '__main__':
    app=create_app(config_dict['dev'])
    app.run()