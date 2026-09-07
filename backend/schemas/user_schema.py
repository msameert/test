from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=4, max=30),
            validate.Regexp(
                r"^[A-Za-z0-9_.-]+$",
                error="Username contains invalid characters.")
        ]
 )

    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128)
    )