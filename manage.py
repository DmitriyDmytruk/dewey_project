import json
import os
import sys

from flask_script import Command, Manager

from webapp import create_app, db
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
                role = RoleModel(**role_data)
                db.session.add(role)

            for role, permissions in data["role_permissions"].items():
                role = db.session.query(RoleModel).filter_by(title=role).one()
                permissions_list = []
                for permission in permissions:
                    permission_item = (
                        db.session.query(PermissionModel)
                        .filter_by(title=permission)
                        .one()
                    )
                    permissions_list.append(permission_item)
                role.permissions = permissions_list
                db.session.add(role)

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


manager.add_command("createrolepermission", RolePermissionCreate())
manager.add_command("createuser", UserCreate())


if __name__ == "__main__":
    manager.run()
