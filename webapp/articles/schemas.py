from marshmallow import Schema, fields


class TagSchema(Schema):
    """
    Tag schema
    """

    id = fields.Int()
    name = fields.String()


class CategorySchema(Schema):
    """
    Category schema
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
    citation = fields.String()
    cfr40_part280 = fields.String()
    local_regulation = fields.String()
    abstract = fields.String()
    categories = fields.List(fields.Nested(CategorySchema))
    reference_images = fields.String()
    effective_date = fields.Date()
    updated_date = fields.Date()
    tags = fields.List(fields.Nested(TagSchema))
    state = fields.String()
