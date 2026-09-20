from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=4, max=30),
            validate.Regexp(
                r"^(?!.*(?:['\";]|--|/\*|\*/|SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|UNION|OR\s+1\s*=\s*1|EXEC))[A-Za-z0-9_.-@]+$",
                error="Username contains invalid characters or unsafe SQL patterns."
            )
        ]
    )

    password = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(min=3, max=128),
            validate.Regexp(
                r"^(?!.*(?:['\";]|--|/\*|\*/|SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|UNION|OR\s+1\s*=\s*1|EXEC)).+$",
                error="Password contains unsafe characters or SQL patterns."
            )
        ]
    )
