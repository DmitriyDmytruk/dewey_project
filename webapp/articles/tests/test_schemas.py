from typing import Dict, Union

from webapp.articles.models import ArticleModel, CategoryModel, TagModel
from webapp.articles.schemas import (
    ArticlePutPostSchema,
    ArticleSchema,
    CategorySchema,
    TagSchema,
)


def test_tag_shema(session):
    """
    Testing [de]serialization with TagSchema
    """
    tag_data: Dict[str, Union[str, int]] = {"name": "Tag", "id": 1}
    tag = TagSchema().load(tag_data, session=session)
    assert tag.name == tag_data.get("name")

    tag: TagModel = session.query(TagModel).filter_by(name="Tag").one()
    data = TagSchema().dump(tag)
    assert data.get("name") == tag.name


def test_category_shema(session):
    """
    Testing [de]serialization with CategorySchema
    """
    category_data: Dict[str, Union[str, int]] = {"name": "Category", "id": 1}
    category = CategorySchema().load(category_data, session=session)
    assert category.name == category_data.get("name")

    category: CategoryModel = session.query(CategoryModel).filter_by(
        name="Category"
    ).one()
    data = CategorySchema().dump(category)
    assert data.get("name") == category.name


def test_article_shema(session):
    """
    Testing [de]serialization with ArticleSchema
    """
    tag: TagModel = session.query(TagModel).filter_by(name="Test tag")
    article_data: Dict[str, Union[str, list]] = {
        "title": "Test title",
        "tags": TagSchema(only=("id",)).dump(tag, many=True),
        "citation": "citation1",
        "cfr40_part280": "cfr40_part2801",
        "unique_id": "unique_id1",
        "legal_language": "legal_language",
    }
    article = ArticlePutPostSchema(partial=True).load(
        article_data, session=session
    )
    assert article.title == article_data["title"]
    assert article.tags[0].name == "Test tag"

    article: ArticleModel = session.query(ArticleModel).filter_by(
        title="Test article"
    )
    data = ArticleSchema().dump(article, many=True)
    assert "title" in data[0] and "tags" in data[0]
    assert data[0]["title"] == "Test article"
    assert data[0]["tags"][0]["name"] == "Test tag"
