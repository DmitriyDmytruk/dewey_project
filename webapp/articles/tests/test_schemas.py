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
