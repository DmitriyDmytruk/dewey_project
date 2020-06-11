articles_retrieve_docstring = """
        Retrieve articles
        ---
        responses:
          200:
            description: Articles retrieved
            schema:
              $ref: '#/definitions/ArticleSchema'
          400:
            description: Invalid request
            schema:
              id: Invalid
              properties:
                message:
                  type: string
                  default: Invalid request
          404:
            description: Not exist
            schema:
              id: NotExist
              properties:
                message:
                  type: string
                  default: Article does not exist.
          500:
            description: Fail
            schema:
              id: Fail
              properties:
                message:
                  type: string
        """


article_update_docstring = """
        Update article
        ---
        parameters:
          - in: body
            name: data
            schema:
              $ref: '#/definitions/ArticlePutPostSchema'
          - in: path
            name: article_id
            type: string
            required: true
        responses:
          200:
            description: Article updated
            schema:
              id: Successful
              properties:
                message:
                  type: string
                  default: Article updated
          400:
            description: Invalid request
            schema:
              id: Invalid
              properties:
                message:
                  type: string
                  default: Invalid request
          404:
            description: Not exist
            schema:
              id: NotExist
              properties:
                message:
                  type: string
                  default: Article does not exist.
          500:
            description: Fail
            schema:
              id: Fail
              properties:
                message:
                  type: string
        """

article_create_docstring = """
        Create article
        ---
        parameters:
          - in: body
            name: data
            schema:
              $ref: '#/definitions/ArticlePutPostSchema'
        responses:
          200:
            description: Article created
            schema:
              id: Successful created
              properties:
                message:
                  type: string
                  default: Article created.
                id:
                  type: integer
          400:
            description: Invalid request
            schema:
              id: Invalid
              properties:
                message:
                  type: string
                  default: Invalid request
          500:
            description: Fail
            schema:
              id: Fail
              properties:
                message:
                  type: string
        """

article_download_docstring = """
        Download article
        ---
        parameters:
          - in: path
            name: article_id
            type: string
            required: true
        responses:
          200:
            description: Download file
            schema:
              id: Successful
              properties:
                file:
                  type: file
                  description: .xls file
          404:
            description: Not exist
            schema:
              id: NotExist
              properties:
                message:
                  type: string
                  default: Article does not exist.
        """