from flask import Flask
from datetime import datetime
from pathlib import Path
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

root_dir = Path(__file__).parent.parent
template_dir = root_dir / 'resources/templates'

app = Flask(__name__, template_folder=template_dir,static_url_path='/static', static_folder='../resources/static')

app.config.from_object(Config)


login_manager=LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = 'Inicie sesión para acceder a esta página'

db = SQLAlchemy(app) #ligar la bd a nuestra aplicacion
migrate = Migrate(app, db)


from app.producto import productoModel,   productoRouter
from app.category import categoryModel,   categoryRouter
from app.carrito import carritoModel,   carritoRouter
from app.factura import facturaModel, facturaRouter
from app.auth import userModel
#from app.auth import authRouter #logeo manual con sesion
from app.fauth import fauthRouter #ñpgueo con libreria
from app.home import homeRouter #ñpgueo con libreria


# if __name__ == '__main__':
#   app.run()
