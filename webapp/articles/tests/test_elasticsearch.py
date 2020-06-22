import pytest
from elasticsearch.exceptions import NotFoundError

from webapp import db, es
from webapp.articles.models import ArticleModel


ARTICLE_INDEX = ArticleModel.__tablename__


@pytest.mark.xfail
def test_new_tag(app):
    """
    Test for Article index create
    """
    with app.app_context():
        db.create_all()
    article_title: str = "ES title"
    new_article = ArticleModel(
        title=article_title,
        tags=[],
        categories=[],
        unique_id="unique_id2",
        citation="citation",
        cfr40_part280="cfr40_part280",
        legal_language="en",
    )
    db.session.add(new_article)
    db.session.commit()

    with pytest.raises(NotFoundError) as error:
        es.get(ARTICLE_INDEX, 0)
    assert error.value.status_code == 404
    resp = es.get(ARTICLE_INDEX, new_article.id)
    assert resp.get("_source").get("id") == new_article.id
    assert resp.get("_source").get("title") == article_title


@pytest.mark.xfail
def test_update_article_index(app):
    """
    Test for update Article index
    """
    with app.app_context():
        db.create_all()
    new_article = ArticleModel(
        title="ES title",
        tags=[],
        categories=[],
        unique_id="unique_id2",
        citation="citation",
        cfr40_part280="cfr40_part280",
        legal_language="en",
    )
    db.session.add(new_article)
    db.session.commit()

    new_title: str = "Updated title"
    new_article.title = new_title
    new_article.tags = new_article.categories = []
    db.session.commit()

    resp = es.get(ARTICLE_INDEX, new_article.id)
    assert resp.get("_source").get("title") == new_title


@pytest.mark.xfail
def test_delete_article_index(app):
    """
    Test for delete Article index
    """
    with app.app_context():
        db.create_all()
    new_article = ArticleModel(
        title="ES title",
        tags=[],
        categories=[],
        unique_id="unique_id2",
        citation="citation",
        cfr40_part280="cfr40_part280",
        legal_language="en",
    )
    db.session.add(new_article)
    db.session.commit()
    db.session.delete(new_article)
    db.session.commit()

    resp = es.search(
        index=ARTICLE_INDEX, body={"query": {"term": {"title": "ES title"}}}
    )
    assert not resp["hits"]["total"]["value"]
