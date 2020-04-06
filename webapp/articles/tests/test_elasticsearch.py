import pytest
from elasticsearch.exceptions import NotFoundError

from webapp import es
from webapp.articles.models import ArticleModel


ARTICLE_INDEX = ArticleModel.__tablename__


@pytest.mark.xfail
def test_new_tag(db):
    """
    Test for Article index create
    """
    article_title = "ES title"
    new_article = ArticleModel(title=article_title)
    db.session.add(new_article)
    db.session.commit()

    with pytest.raises(NotFoundError) as e:
        es.get("articles", 0)
    assert e.value.status_code == 404

    resp = es.get(ARTICLE_INDEX, new_article.id)
    assert resp.get("_source").get("id") == new_article.id
    assert resp.get("_source").get("title") == article_title


@pytest.mark.xfail
def test_update_article_index():
    """
    Test for update Article index
    """
    new_title = "Updated title"
    article = ArticleModel.query.first()
    resp = es.update(
        index=ARTICLE_INDEX,
        doc_type="_doc",
        id=article.id,
        body={"doc": {"title": new_title}},
    )
    assert resp["result"] == "updated"

    resp = es.get(ARTICLE_INDEX, article.id)
    assert resp.get("_source").get("title") == new_title


@pytest.mark.xfail
def test_delete_article_index():
    """
    Test for delete Article index
    """
    article = ArticleModel.query.first()
    es.delete(ARTICLE_INDEX, article.id)
    with pytest.raises(NotFoundError) as e:
        es.get(ARTICLE_INDEX, article.id)
    assert e.value.status_code == 404


@pytest.mark.xfail
def test_search_article_by_index():
    """
    Test for search Article
    """
    resp = es.search(
        index=ARTICLE_INDEX, body={"query": {"match": {"title": "ES"}}}
    )
    assert resp["hits"]["hits"][0]["_source"]["title"] == "ES title"
