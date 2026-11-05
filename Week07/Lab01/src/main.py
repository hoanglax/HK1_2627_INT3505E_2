from pydoc import text

from flask import Flask, app
from sqlalchemy import text

from src.extensions import db, migrate, api
from src.config import Config
from src.models import Product, Order, OrderItem
from src.api.products import blp as products_blp
from src.api.orders import blp as orders_blp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    api.register_blueprint(products_blp)
    api.register_blueprint(orders_blp)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    @app.get("/ready")
    def ready():
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ready", "database": "connected"}, 200
        except Exception as error:
            print("DATABASE ERROR:", error)
            return {"status": "not ready", "database": "disconnected"}, 503

    return app