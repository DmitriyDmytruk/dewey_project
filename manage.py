import json
import os
import sys

from flask_script import Command, Manager

from webapp import create_app, db
from webapp.articles.models import ArticleModel, CategoryModel
from webapp.users.models import PermissionModel, RoleModel, UserModel


env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app("config.%sConfig" % env.capitalize())
manager = Manager(app)


class RolePermissionCreate(Command):
    """
    Creates default role and permission
    """

    def run(self):
        try:
            f = open("webapp/utils/fixtures/role_permission.json")
            data = json.loads(f.read())

            for permission_data in data["permissions"]:
                permission = PermissionModel(title=permission_data)
                db.session.add(permission)

            for role_data in data["roles"]:
                role = RoleModel(title=role_data["title"])
                if role_data.get("role_permissions"):
                    permissions = db.session.query(PermissionModel).filter(
                        PermissionModel.title.in_(
                            role_data.get("role_permissions")
                        )
                    )
                    role.permissions = permissions.all()
                db.session.add(role)

            db.session.commit()
            sys.__stdout__.write("\033[32mRole and permission created\n")
        except Exception as error:
            sys.__stdout__.write("\033[31mNot created: " + str(error) + "\n")


class UserCreate(Command):
    """
    Creates default role and permission
    """

    def run(self):
        try:
            f = open("webapp/utils/fixtures/initial_user.json")
            data = json.loads(f.read())

            user_data = data["user"]

            role_id = None
            role = RoleModel.query.filter_by(title=data["role_title"]).first()
            if role:
                role_id = role.id

            user = UserModel(**user_data, **{"role_id": role_id})

            db.session.add(user)
            db.session.commit()
            sys.__stdout__.write("\033[32mUser created\n")
        except Exception as error:
            sys.__stdout__.write("\033[31mNot created: " + str(error) + "\n")


class ArticlesCreate(Command):
    """
    Creates default articles
    """

    def run(self):
        try:
            f = open("webapp/utils/fixtures/initial_articles.json")
            data = json.loads(f.read())

            categories_data = data["categories"]
            for category in categories_data:
                db.session.add(CategoryModel(name=category))

            articles_data = data["articles"]
            for article in articles_data:
                article_categories = db.session.query(CategoryModel).filter(
                    CategoryModel.name.in_(article["categories"])
                )
                new_article = ArticleModel(**article)
                new_article.categories = article_categories.all()
                db.session.add(new_article)

            db.session.commit()
            sys.__stdout__.write("\033[32mArticles created\n")
        except Exception as error:
            sys.__stdout__.write("\033[31mNot created: " + str(error) + "\n")


manager.add_command("create_role_permission", RolePermissionCreate())
manager.add_command("create_user", UserCreate())
manager.add_command("create_articles", ArticlesCreate())


if __name__ == "__main__":
    manager.run()
