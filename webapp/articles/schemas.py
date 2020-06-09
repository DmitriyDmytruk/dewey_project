from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema, fields as sqlalchemy_fields

from .models import ArticleModel, CategoryModel, TagModel


class TagSchema(ModelSchema):
    """
    Tag schema
    """

    class Meta:
        """
        MetaClass for Tag Schema
        """

        model: TagModel = TagModel


class CategorySchema(ModelSchema):
    """
    Category schema
    """

    class Meta:
        """
        MetaClass for Category Schema
        """

        model: CategoryModel = CategoryModel


class ArticleSchema(ModelSchema):
    """
    ArticleModel BaseSchema
    """

    id = fields.Int(dump_only=True)
    tags = sqlalchemy_fields.Nested(TagSchema, many=True)
    categories = sqlalchemy_fields.Nested(CategorySchema, many=True)

    class Meta:
        """
        MetaClass for Article Schema
        """

        model = ArticleModel


class ArticlePutPostSchema(ArticleSchema):
    """
    Schema for put/post methods for Article Model
    """

    tags = sqlalchemy_fields.Nested(TagSchema, many=True, only=["id"])
    categories = sqlalchemy_fields.Nested(
        CategorySchema, many=True, only=["id"]
    )
