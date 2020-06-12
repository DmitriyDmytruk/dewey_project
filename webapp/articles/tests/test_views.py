import os

from flask import Response, url_for
from werkzeug.datastructures import FileStorage

import json

from webapp.articles.models import ArticleModel
from webapp.users.models import PermissionModel, UserModel


def test_retrieve_articles(client, session):
    """
    Test articles retrieve api view
    :param client:
    :param session:
    :return:
    """
    response = client.get(url_for("articles.articles"))
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    response = client.get(
        url_for("articles.articles"),
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
        url_for("articles.articles"),
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.json.get("message") == "Access denied."
    assert response.json.get("status") == 403

    user1: UserModel = session.query(UserModel).filter_by(
        email="test@gmail.com"
    ).one()
    jwt_token: str = user1.encode_auth_token().decode("utf-8")
    response = client.get(
        url_for("articles.articles"),
        headers={"Authorization": f"Token {jwt_token}"},
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


def file_upload(filename: str, content_type: str, jwt_token: str, client):
    """BL for `test_article_upload` successful"""
    file_path: str = os.path.join(f"webapp/articles/tests/{filename}")

    xls_file: FileStorage = FileStorage(
        stream=open(file_path, "rb"),
        filename=f"{filename}",
        content_type=f"{content_type}",
    )
    data = {"file": xls_file}
    response: Response = client.post(
        url_for("articles.upload"),
        data=data,
        follow_redirects=True,
        content_type="multipart/form-data",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    return response


def test_article_upload(client, session):
    """Uploading csv/xls file."""
    response: Response = client.post(
        url_for("articles.upload"),
        follow_redirects=True,
        content_type="multipart/form-data",
    )
    assert response.json.get("message") == "Provide a valid auth token."
    assert response.json.get("status") == 401

    response: Response = client.post(
        url_for("articles.upload"),
        follow_redirects=True,
        content_type="multipart/form-data",
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
    response: Response = client.post(
        url_for("articles.upload"),
        follow_redirects=True,
        content_type="multipart/form-data",
        headers={"Authorization": f"Token {jwt_token}"},
    )
    assert response.json.get("message") == "Access denied."
    assert response.json.get("status") == 403

    user1: UserModel = session.query(UserModel).filter_by(
        email="test@gmail.com"
    ).one()
    jwt_token: str = user1.encode_auth_token().decode("utf-8")
    user1.role.permissions.append(
        session.query(PermissionModel)
        .filter_by(title="can_view_articles")
        .first()
    )

    response: Response = file_upload(
        "for_test.xls", "application/vnd.ms-excel", jwt_token, client
    )
    assert response.status_code == 200
    assert response.json.get("message") == "File uploaded."

    response: Response = file_upload(
        "for_test.csv", "text/csv", jwt_token, client
    )
    assert response.status_code == 200
    assert response.json.get("message") == "File uploaded."

    response: Response = file_upload(
        "for_test.txt", "text/plain", jwt_token, client
    )
    assert response.status_code == 400
    assert response.json.get("message") == "Extension of file not allowed"


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
