from flask.views import MethodView
from flask_smorest import Blueprint, abort

from src.extensions import db
from src.models import Order, OrderItem, Product
from src.schemas.orders import OrderCreateSchema, OrderSchema


blp = Blueprint(
    "Orders",
    "orders",
    url_prefix="/api/v1/orders",
    description="Operations on orders"
)

@blp.route("/")
class OrdersList(MethodView):

    @blp.arguments(OrderCreateSchema, location="json")
    @blp.response(201, OrderSchema)
    def post(self, order_data):

        order = Order(status="pending")
        db.session.add(order)

        for item_data in order_data["items"]:
            product = Product.query.filter_by(
                id=item_data["product_id"],
                is_archived=False
            ).first()

            if product is None:
                db.session.rollback()
                abort(
                    404,
                    message=f"Product {item_data['product_id']} not found."
                )

            order_item = OrderItem(
                order=order,
                product=product,
                quantity=item_data["quantity"],
                unit_price=product.price_cents
            )

            db.session.add(order_item)

        db.session.commit()

        return order

from sqlalchemy.orm import selectinload

@blp.route("/<int:order_id>")
class OrderDetail(MethodView):

    @blp.response(200, OrderSchema)
    def get(self, order_id):
        order = (
            Order.query
            .options(
                selectinload(Order.items).selectinload(OrderItem.product)
            )
            .filter_by(id=order_id)
            .first_or_404()
        )

        return order