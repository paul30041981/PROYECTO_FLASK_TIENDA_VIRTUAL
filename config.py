import os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

#base_dir = os.path.abspath(os.path.dirname(__file__))

db = os.getenv('DATABASE_NAME')
user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASS')
host = os.getenv('DATABASE_HOST')
port = os.getenv('DATABASE_PORT')


class Config(object):
    # sqlite:////tmp/test.db
    # mysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = f'postgres://{user}:{password}@{host}:{port}/{db}'
    # SQLALCHEMY_DATABASE_URI = f'''sqlite:///{Path('.')}/test.db'''
    SQLACHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECRET_KEY = 'pachaqtec'

