from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    sku = fields.String(required=True, validate=validate.Length(min=3, max=32))

    name = fields.String(required=True, validate=validate.Length(min=1, max=256))

    price_cents = fields.Int(required=True, validate=validate.Range(min=0)) 

    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))