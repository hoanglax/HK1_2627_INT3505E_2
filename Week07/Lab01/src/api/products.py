from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.schemas import products
from src.extensions import db
from src.models import Product
from src.schemas.products import (ProductSchema, 
                                  ProductListSchema, 
                                  PaginationSchema,
                                  ProductUpdateSchema,
                                  ProductReserveSchema)

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

    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    def get(self, pagination_data):
        page = Product.query.filter_by(is_archived=False).paginate(
            page = pagination_data["page"],
            per_page = pagination_data["per_page"],
            error_out = False
        )

        return {
            "items": page.items,
            "total": page.total,
            "page": page.page,
            "per_page": page.per_page
        }

    @blp.route("/<int:product_id>")
    class ProductDetail(MethodView):

        @blp.response(200, ProductSchema)
        def get(self, product_id):
            product = Product.query.filter_by(id=product_id, is_archived=False).first_or_404()
            return product
        
        @blp.arguments(ProductUpdateSchema, location="json")
        @blp.response(200, ProductSchema)
        def patch(self, product_data, product_id):
            product = Product.query.get_or_404(product_id)

            if "sku" in product_data:
                existing_product = Product.query.filter_by(sku=product_data["sku"]).first()
                
                if existing_product and existing_product.id != product_id:
                    abort(409, message="SKU already exists.")

            for key, value in product_data.items():
                setattr(product, key, value)

            db.session.commit()

            return product

        @blp.response(204)
        def delete(self, product_id):
            product = Product.query.get_or_404(product_id)
            product.is_archived = True
            db.session.commit()
            return ""

    @blp.route("/<int:product_id>/reserve")
    class ProductReserve(MethodView):
        @blp.arguments(ProductReserveSchema, location="json")
        @blp.response(200, ProductSchema)
        def post(self, reserve_data, product_id):
            product = Product.query.filter_by(id=product_id, is_archived=False).first_or_404()

            quantity = reserve_data["quantity"]

            if product.qty_in_stock < quantity:
                abort(409, message=f"Not enough stock. Available: {product.qty_in_stock}")

            product.qty_in_stock -= quantity
            db.session.commit()

            return product