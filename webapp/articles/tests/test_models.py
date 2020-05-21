import pytest
from sqlalchemy.exc import IntegrityError

from webapp.articles.models import ArticleModel, TagModel


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
    with pytest.raises(IntegrityError) as e:
        session.commit()
    assert e.typename == "IntegrityError"


def test_new_article(session):
    """
    Test for Article create
    """
    article_title: str = "Test article"
    new_article: ArticleModel = ArticleModel(
        title=article_title,
        legal_language="en",
        abstract="",
        unique_id="unique_id1",
        citation="citation",
        cfr40_part280="cfr40_part280",
    )
    session.add(new_article)
    session.commit()


def test_delete_tag(session):
    """
    Test for Tag delete
    """
    start_count: int = session.query(TagModel).count()
    tag: TagModel = session.query(TagModel).first()
    session.delete(tag)
    session.commit()
    assert start_count == TagModel.query.count() + 1


def test_delete_article(session):
    """
    Test for Article delete
    """
    start_count: int = ArticleModel.query.count()
    article: ArticleModel = session.query(ArticleModel).first()
    session.delete(article)
    session.commit()
    assert start_count == ArticleModel.query.count() + 1


def test_update_tag(session):
    """
    Test for Tag update
    """
    new_name: str = "New name"
    tag: TagModel = session.query(TagModel).first()
    tag.name = new_name
    session.add(tag)
    session.commit()
    assert tag.name == "New name"


def test_update_article(session):
    """
    Test for Article update
    """
    new_title: str = "New title"
    article: ArticleModel = session.query(ArticleModel).first()
    article.title = new_title
    session.add(article)
    session.commit()
    assert article.title == "New title"
