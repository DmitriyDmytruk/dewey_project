from flask import url_for

from webapp.users.models import UserModel


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
