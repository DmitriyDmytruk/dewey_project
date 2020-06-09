from webapp.articles.models import ArticleModel
from webapp.users.models import PermissionModel, UserModel


def test_retrieve_articles(client, session):
    """
    Test articles retrieve api view (with decorators)
    :param client:
    :param session:
    :return:
    """
    response = client.get("/articles")
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    response = client.get(
        "/articles", headers={"Authorization": "Token WrongToken"}
    )
    assert (
        response.json.get("message") == "Invalid token. Please log in again."
    )
    assert response.json.get("status") == 401

    user2: UserModel = session.query(UserModel).filter_by(
        email="test2@gmail.com"
    ).one()
    jwt_token: str = user2.encode_auth_token().decode("utf-8")
    response = client.get(
        "/articles", headers={"Authorization": f"Token {jwt_token}"}
    )
    assert response.json.get("message") == "Access denied."
    assert response.json.get("status") == 403

    user1: UserModel = session.query(UserModel).filter_by(
        email="test@gmail.com"
    ).one()
    jwt_token: str = user1.encode_auth_token().decode("utf-8")
    response = client.get(
        "/articles", headers={"Authorization": f"Token {jwt_token}"}
    )
    assert response.status_code == 200


def test_download_articles(client, session):
    """
    Test articles retrieve api view (with decorators)
    :param client:
    :param session:
    :return:
    """
    article: ArticleModel = ArticleModel.query.first()
    article_id: int = article.id
    response = client.get(f"/articles/{article_id}/download")
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    response = client.get(
        f"/articles/{article_id}/download",
        headers={"Authorization": "Token WrongToken"},
    )
    assert (
        response.json.get("message") == "Invalid token. Please log in again."
    )
    assert response.json.get("status") == 401

    user2: UserModel = session.query(UserModel).filter_by(
        email="test2@gmail.com"
    ).one()
    jwt_token: str = user2.encode_auth_token().decode("utf-8")
    response = client.get(
        f"/articles/{article_id}/download",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.json.get("message") == "Access denied."
    assert response.json.get("status") == 403

    user: UserModel = UserModel.query.first()
    jwt_token: str = user.encode_auth_token().decode("utf-8")
    permission: PermissionModel = PermissionModel.query.filter_by(
        title="can_view_articles"
    ).first()
    user.role.permissions.append(permission)
    response = client.get(
        f"/articles/999999/download",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 404
    assert response.json.get("message") == "Article does not exist."

    response = client.get(
        f"/articles/{article_id}/download",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert "attachment; filename=Test article.xls" in list(
        response.headers.values()
    )
    assert response.content_type == "application/vnd.ms-excel"
