login_docstring = """
        User Login
        ---
        tags:
          - users
        parameters:
          - in: body
            name: data
            schema:
              id: Login
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  description: email for user
                password:
                  type: string
                  description: user password
        responses:
          200:
            description: Login successful
            schema:
              id: Successful
              properties:
                status:
                  type: string
                  default: success
                message:
                  type: string
                  default: Successfully logged in.
                auth_token:
                  type: string
          404:
            description: User does not exist
            schema:
              id: Not found
              properties:
                status:
                  type: string
                  default: fail
                message:
                  type: string
                  default: User does not exist.
          500:
            description: Error
            schema:
              id: Not found
              properties:
                status:
                  type: string
                  default: fail
                message:
                  type: string
                  default: Try again
        """


user_create_docstring = """
        Create a new user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: data
            schema:
              id: UserModel
              required:
                - email
                - role
              properties:
                email:
                  type: string
                  description: email for user
                role:
                  schema:
                    id: RoleModel
                    required:
                      - title
                    properties:
                      title:
                        type: string
                        description: title of role
        responses:
          201:
            description: User created
        """
