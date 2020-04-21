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
    article_title = "ES title"
    new_article = ArticleModel(
        title=article_title,
        tags=[],
        categories=[],
        unique_id="unique_id2",
        citation="citation",
        cfr40_part280="cfr40_part280",
        legal_language="en",
    )
    with app.app_context():
        db.create_all()
    db.session.add(new_article)
    db.session.commit()

    with pytest.raises(NotFoundError) as e:
        es.get("articles", 0)
    assert e.value.status_code == 404

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
    new_title = "Updated title"
    article = ArticleModel.query.first()
    article.title = new_title
    article.tags = []
    article.categories = []

    db.session.add(article)
    db.session.commit()

    resp = es.get(ARTICLE_INDEX, article.id)
    assert resp.get("_source").get("title") == new_title


@pytest.mark.xfail
def test_delete_article_index(app):
    """
    Test for delete Article index
    """
    with app.app_context():
        db.create_all()
    ArticleModel.reindex()
    article = ArticleModel.query.first()
    db.session.delete(article)
    db.session.commit()
    resp = es.search(
        index=ARTICLE_INDEX, body={"query": {"match": {"id": article.id}}}
    )
    assert not resp["hits"]["total"]["value"]
