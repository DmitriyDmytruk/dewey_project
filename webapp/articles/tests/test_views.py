import json

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


def test_create_article(client):
    """
    Test article create api view (with decorators)
    :param client:
    :param session:
    :return:
    """
    response = client.post("/articles")
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    user: UserModel = UserModel.query.order_by(UserModel.id.desc()).first()
    response = client.post(
        "/articles",
        data=json.dumps(
            {
                "title": "Test title",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id1",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": "Token WrongToken"},
    )
    assert (
        response.json.get("message") == "Invalid token. Please log in again."
    )
    assert response.json.get("status") == 401

    jwt_token = user.encode_auth_token().decode("utf-8")
    response = client.post(
        "/articles",
        data=json.dumps(
            {
                "title": "Test title",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id1",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.json.get("message") == "Access denied."
    assert response.json.get("status") == 403

    user2 = UserModel.query.first()
    jwt_token: str = user2.encode_auth_token().decode("utf-8")
    user2.role.permissions.append(PermissionModel(title="can_add_articles"))
    response = client.post(
        "/articles", data={}, headers={"Authorization": f"Token {jwt_token}"}
    )
    assert response.status_code == 400
    assert response.json.get("message") == "Invalid request"

    response = client.post(
        "/articles",
        data=json.dumps(
            {
                "title": "Test title1",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id2",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert response.json.get("message") == "Article created"

    response = client.post(
        "/articles",
        data=json.dumps(
            {
                "title": "Test title",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 500


def test_update_article(client):
    """
    Test article update api view (with decorators)
    :param client:
    :param session:
    :return:
    """
    article: ArticleModel = ArticleModel.query.first()
    article_id: int = article.id
    response = client.put(f"/articles/{article_id}")
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    user: UserModel = UserModel.query.order_by(UserModel.id.desc()).first()
    response = client.put(
        f"/articles/{article_id}",
        data=json.dumps(
            {
                "title": "Test title",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id1",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": "Token WrongToken"},
    )
    assert (
        response.json.get("message") == "Invalid token. Please log in again."
    )
    assert response.json.get("status") == 401

    jwt_token = user.encode_auth_token().decode("utf-8")
    response = client.put(
        f"/articles/{article_id}",
        data=json.dumps(
            {
                "title": "Test title",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id1",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.json.get("message") == "Access denied."
    assert response.json.get("status") == 403

    user2 = UserModel.query.first()
    jwt_token: str = user2.encode_auth_token().decode("utf-8")
    user2.role.permissions.append(PermissionModel(title="can_change_articles"))
    response = client.put(
        f"/articles/{article_id}",
        data={},
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 400
    assert response.json.get("message") == "Invalid request"

    response = client.put(
        "/articles/999999999",
        data=json.dumps(
            {
                "title": "Test title1",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id2",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 404
    assert response.json.get("message") == "Article does not exist."

    response = client.put(
        f"/articles/{article_id}",
        data=json.dumps(
            {
                "title": "Test title1",
                "citation": "citation2",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id4",
                "legal_language": "legal_language",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 200
    assert response.json.get("message") == "Article updated"
    assert article.citation == "citation2"

    response = client.put(
        f"/articles/{article_id}",
        data=json.dumps(
            {
                "title": "Test title",
                "citation": "citation1",
                "cfr40_part280": "cfr40_part2801",
                "unique_id": "unique_id",
                "legal_language": "legal_language",
                "tags": "",
            }
        ),
        content_type="application/json",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.status_code == 500
