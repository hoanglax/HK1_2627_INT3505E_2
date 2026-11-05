from marshmallow import Schema, fields, validate


class OrderItemCreateSchema(Schema):
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )


class OrderCreateSchema(Schema):
    items = fields.List(
        fields.Nested(OrderItemCreateSchema),
        required=True,
        validate=validate.Length(min=1)
    )

class ProductInOrderSchema(Schema):
    id = fields.Integer(dump_only=True)
    sku = fields.String(dump_only=True)
    name = fields.String(dump_only=True)
    price_cents = fields.Integer(dump_only=True)

class OrderItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    product_id = fields.Integer()
    quantity = fields.Integer()
    unit_price = fields.Integer(dump_only=True)
    product = fields.Nested(ProductInOrderSchema, dump_only=True)


class OrderSchema(Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String(dump_only=True)
    items = fields.List(
        fields.Nested(OrderItemSchema),
        dump_only=True
    )