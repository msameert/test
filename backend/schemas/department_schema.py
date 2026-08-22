from marshmallow import schema, fields, validate

class DepartmentSchema(schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2,max=50)
        )
    code = fields.Str(
        required=True,
        validate=validate.Length(min=1,max=7)
    )