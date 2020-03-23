from webapp.articles.models import ArticleModel, TagModel


def test_new_tag():
    """
    Test for Tag create
    """
    tag_name = "Tag"
    new_tag = TagModel(name=tag_name)
    assert new_tag.name == tag_name


def test_new_article():
    """
    Test for Article create
    """
    article_title = "Test article"
    new_article = ArticleModel(
        title=article_title, legal_language="en", abstract=""
    )
    assert new_article.title == article_title
