import pytest
from sqlalchemy.exc import IntegrityError

from webapp.articles.models import ArticleModel, CategoryModel, TagModel


def test_new_tag(session):
    """
    Test for Tag create
    """
    tag_name: str = "Tag"
    new_tag: TagModel = TagModel(name=tag_name)
    session.add(new_tag)
    session.commit()
    assert new_tag.name == tag_name

    tag_name: str = "Test tag"
    new_tag: TagModel = TagModel(name=tag_name)
    session.add(new_tag)
    with pytest.raises(IntegrityError) as error:
        session.commit()
    assert error.typename == "IntegrityError"
