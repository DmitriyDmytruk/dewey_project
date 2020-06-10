from webapp.articles.models import ArticleModel
from webapp.users.models import PermissionModel, UserModel


def test_retrieve_articles(client, session):
    """
    Test articles retrieve api view
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
    Test articles retrieve api view
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


def test_articles_search(client, session):
    """
    Test articles search api view
    :param client:
    :param session:
    :return:
    """
    ArticleModel.reindex()
    response = client.get("/articles/search")
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    response = client.get(
        "/articles/search", headers={"Authorization": "Token WrongToken"},
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
        "/articles/search", headers={"Authorization": f"Token {jwt_token}"},
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
        "/articles/search", headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert sorted(response.json.keys()) == [
        "categories",
        "response",
        "states",
        "tags",
    ]
    assert (
        isinstance(response.json["categories"], list)
        and isinstance(response.json["tags"], list)
        and isinstance(response.json["states"], list)
        and isinstance(response.json["response"], list)
    )

    response = client.get(
        "/articles/search",
        json={"state": "Alaska"},
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert len(response.json["response"]) == 1
    assert response.json["response"][0]["state"] == "Alaska"

    response = client.get(
        "/articles/search",
        json={"categories": ["Applicability"]},
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert len(response.json["response"]) == 5
    assert "Applicability" in response.json["response"][0]["categories"]

    response = client.get(
        "/articles/search",
        json={"state": "Alaska", "categories": ["Applicability"]},
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert len(response.json["response"]) == 1
    assert "Applicability" in response.json["response"][0]["categories"]
    assert "Alaska" in response.json["response"][0]["state"]

    response = client.get(
        "/articles/search",
        json={"state": "Ohio", "categories": ["Applicability"]},
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert response.json["response"] == "Articles not found."
