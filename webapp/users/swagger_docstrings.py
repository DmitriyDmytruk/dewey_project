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
            content: 
              application/json:
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
            content: 
              application/json:
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
            content: 
              application/json:
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
        requestBody:
          content:
            application/json:
              schema:
                type: object
                required:
                  - email
                  - role
                properties:
                  email:
                    type: string
                    description: email for user
                  role:
                    $ref: '#/definitions/RoleSchema'
        responses:
          '201':
            description: User created
            content: 
              application/json:
                schema:
                  $ref: '#/definitions/UserSchema'
          '400':
            description: Failed
            content: 
              application/json:
                schema:
                  id: Failed
                  properties:
                    message:
                      type: string
                      default: No input data provided
          '422':
            description: Error
            content: 
              application/json:
                schema:
                  id: Error
                  properties:
                    message:
                      type: string
        """
