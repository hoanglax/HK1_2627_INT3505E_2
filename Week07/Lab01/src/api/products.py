from flask.views import MethodView
from flask_smorest import Blueprint

from src.schemas import products
from src.extensions import db
from src.models import Product
from src.schemas.products import ProductSchema

blp = Blueprint(
    "Products",
    "products",
    url_prefix="/api/v1/products",
    description="Operations on products"
)

@blp.route("/")
class ProductsList(MethodView):
   
    @blp.arguments(ProductSchema, location="json")
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        product = Product(**product_data)
        
        db.session.add(product)
        db.session.commit()

        return products
