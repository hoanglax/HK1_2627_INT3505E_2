from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    
    id = fields.Int(dump_only=True)

    sku = fields.String(required=True, validate=validate.Length(min=3, max=32))

    name = fields.String(required=True, validate=validate.Length(min=1, max=256))

    price_cents = fields.Int(required=True, validate=validate.Range(min=0))

    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))

class ProductListSchema(Schema):
    items = fields.List(fields.Nested(ProductSchema), dump_only=True)
    total = fields.Integer(dump_only=True)
    page = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)

class PaginationSchema(Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=20, validate=validate.Range(min=1, max=100))

class ProductUpdateSchema(Schema):
    sku = fields.String(validate=validate.Length(min=3, max=32))
    name = fields.String(validate=validate.Length(min=1, max=256))
    price_cents = fields.Int(validate=validate.Range(min=0)) 
    qty_in_stock = fields.Int(validate=validate.Range(min=0))

class ProductReserveSchema(Schema):
    quantity = fields.Int(required=True, validate=validate.Range(min=1))