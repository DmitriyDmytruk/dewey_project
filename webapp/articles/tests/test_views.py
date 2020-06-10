import os

from flask import Response, url_for
from werkzeug.datastructures import FileStorage

from webapp.users.models import PermissionModel, UserModel
from webapp.articles.models import ArticleModel
from webapp.users.models import PermissionModel, UserModel


def test_retrieve_articles(client, session):
    """
    Test articles retrieve api view (with decorators)
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
