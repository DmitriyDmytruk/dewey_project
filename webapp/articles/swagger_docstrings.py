articles_retrieve_docstring = """
        Retrieve articles
        ---
        responses:
          200:
            description: Articles retrieved
            content: 
              application/json:
                schema:
                  $ref: '#/definitions/ArticleSchema'
          400:
            description: Invalid request
            content: 
              application/json:
                schema:
                  id: Invalid
                  properties:
                    message:
                      type: string
                      default: Invalid request
          404:
            description: Not exist
            content: 
              application/json:
                schema:
                  id: NotExist
                  properties:
                    message:
                      type: string
                      default: Article does not exist.
          500:
            description: Fail
            content: 
              application/json:
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
          - name: data
            in: body
            schema:
              $ref: '#/definitions/ArticlePutPostSchema'
          - name: article_id
            in: path
            required: true
            schema:
              type: integer
        responses:
          200:
            description: Article updated
            content: 
              application/json:
                schema:
                  id: Successful
                  properties:
                    message:
                      type: string
                      default: Article updated
          400:
            description: Invalid request
            content: 
              application/json:
                schema:
                  id: Invalid
                  properties:
                    message:
                      type: string
                      default: Invalid request
          404:
            description: Not exist
            content: 
              application/json:
                schema:
                  id: NotExist
                  properties:
                    message:
                      type: string
                      default: Article does not exist.
          500:
            description: Fail
            content: 
              application/json:
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
          '200':
            description: Article created
            content: 
              application/json:
                schema:
                  id: Successful created
                  properties:
                    message:
                      type: string
                      default: Article created.
                    id:
                      type: integer
          '400':
            description: Invalid request
            content: 
              application/json:
                schema:
                  id: Invalid
                  properties:
                    message:
                      type: string
                      default: Invalid request
          '500':
            description: Fail
            content: 
              application/json:
                schema:
                  id: Fail
                  properties:
                    message:
                      type: string
        """

articles_search_docstring = """
        Articles search
        ---
        openapi: 3.0.0
        tags: ['articles']
        description: in ``body`` - ``{"state" - "string", "tags" - ["Tag name 1", "Tag name 2"], "categories" - ["Category name 1", "Category name 2"]}``
        responses:
          '200':
            description: Articles found
            content: 
              application/json:
                schema:
                  type: array
                  items:
                    oneOf:
                      - $ref: '#/definitions/ArticleFirstRequestSchema'
                      - $ref: '#/definitions/ArticleSchema'
          '400':
            description: Invalid request
            content: 
              application/json:
                schema:
                  id: Invalid
                  properties:
                    message:
                      type: string
                      default: Invalid request
          '500':
            description: Fail
            content: 
              application/json:
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
            schema:
              type: integer
        responses:
          '200':
            description: Download file
            content: 
              application/json:
                schema:
                  id: Successful
                  properties:
                    file:
                      type: file
                      description: .xls file
          404:
            description: Not exist
            content: 
              application/json:
                schema:
                  id: NotExist
                  properties:
                    message:
                      type: string
                      default: Article does not exist.
        """
