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


def test_new_category(session):
    """
    Test for Category create
    """
    category_name: str = "Category"
    new_category: CategoryModel = CategoryModel(name=category_name)
    session.add(new_category)
    session.commit()
    assert new_category.name == category_name

    category_name: str = "Test category"
    new_category: CategoryModel = CategoryModel(name=category_name)
    session.add(new_category)
    with pytest.raises(IntegrityError) as error:
        session.commit()
    assert error.typename == "IntegrityError"


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


def test_delete_category(session):
    """
    Test for Category delete
    """
    start_count: int = session.query(CategoryModel).count()
    category: CategoryModel = session.query(CategoryModel).first()
    session.delete(category)
    session.commit()
    assert start_count == CategoryModel.query.count() + 1


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


def test_update_category(session):
    """
    Test for Category update
    """
    new_name: str = "New name"
    category: CategoryModel = session.query(CategoryModel).first()
    category.name = new_name
    session.add(category)
    session.commit()
    assert category.name == "New name"


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
