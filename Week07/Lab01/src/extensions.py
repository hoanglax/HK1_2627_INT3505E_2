from flask_smorest import Api # Xay dung REST API
from flask_sqlalchemy import SQLAlchemy # Lam viec voi PostgreSQL
from flask_migrate import Migrate # Quan ly thay doi cau truc database 

db = SQLAlchemy() # Tao extension quan ly database
migrate = Migrate() # Tao extension quan ly thay doi cau truc database
api = Api() # Tao extension quan ly REST API