import json
import os
import sys

from flask_script import Command, Manager

from webapp import create_app, db, migrate
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
            f = open("webapp/users/fixtures/role_permission.json")
            data = json.loads(f.read())

            permission_data = data["permission"]
            permission = PermissionModel(**permission_data)

            role_data = data["role"]
            role = RoleModel(**role_data, **{"permissions": [permission]})

            db.session.add_all([permission, role])
            db.session.commit()
            sys.__stdout__.write("\033[32mRole and permission created\n")
        except Exception as error:
            sys.__stdout__.write("\033[31mNot created: " + str(error) + "\n")
            pass


class UserCreate(Command):
    """
    Creates default role and permission
    """

    def run(self):
        try:
            f = open("webapp/users/fixtures/initial_user.json")
            data = json.loads(f.read())

            user_data = data["user"]

            role_id = None
            role = RoleModel.query.filter_by(title="API User").first()
            if role:
                role_id = role.id

            user = UserModel(**user_data, **{"role_id": role_id})

            db.session.add(user)
            db.session.commit()
            sys.__stdout__.write("\033[32mUser created\n")

        except Exception as error:
            sys.__stdout__.write("\033[31mNot created: " + str(error) + "\n")


manager.add_command("createrolepermission", RolePermissionCreate())
manager.add_command("createuser", UserCreate())


if __name__ == "__main__":
    manager.run()
