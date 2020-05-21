from typing import Dict, Union

from webapp.articles.models import ArticleModel, TagModel
from webapp.articles.schemas import ArticleSchema, TagSchema


def test_tag_shema(session):
    """
    Testing [de]serialization with TagSchema
    """
    tag_data: Dict[str, Union[str, int]] = {"name": "Tag", "id": 1}
    data = TagSchema().load(tag_data)
    assert data.get("name") == tag_data.get("name")

    tag: TagModel = session.query(TagModel).filter_by(name="Test tag").one()
    data = TagSchema().dump(tag)
    assert data.get("name") == tag.name


def test_article_shema(session):
    """
    Testing [de]serialization with ArticleSchema
    """
    tag: TagModel = session.query(TagModel).filter_by(name="Test tag")
    article_data: Dict[str, Union[str, list]] = {
        "title": "Test title",
        "tags": TagSchema().dump(tag, many=True),
    }
    data = ArticleSchema().load(article_data)
    assert "title" in data and "tags" in data
    assert data["title"] == article_data["title"]
    assert data["tags"][0]["name"] == "Test tag"

    article: ArticleModel = session.query(ArticleModel).filter_by(
        title="Test article"
    )
    data = ArticleSchema().dump(article, many=True)
    assert "title" in data[0] and "tags" in data[0]
    assert data[0]["title"] == "Test article"
    assert data[0]["tags"][0]["name"] == "Test tag"
