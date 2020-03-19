from flask import Blueprint, request

from .models import ArticleModel


articles_blueprint = Blueprint("articles", __name__, url_prefix="/articles")
