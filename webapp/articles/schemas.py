from marshmallow import Schema, fields


class TagSchema(Schema):
    """
    Tag schema
    """

    id = fields.Int()
    name = fields.String()


class ArticleSchema(Schema):
    """
    Article schema
    """

    id = fields.Int()
    title = fields.String()
    legal_language = fields.String()
    abstract = fields.String()
    effective_date = fields.DateTime()
    updated_date = fields.DateTime()
    state = fields.String()
    tags = fields.List(fields.Nested(TagSchema))
