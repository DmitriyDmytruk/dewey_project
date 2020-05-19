file_upload_docstring = """
        Read xls/csv file
        ---
        tags:
          - File upload
        consumes:
          - multipart/form-data
        parameters:
          - in: formData
            name: file
            type: file
            description: Upload file.
          - in: formData
            name: data
            type: dict
            description: Extra data.
        responses:
          200:
            description: File uploaded
            schema:
              id: Successful
              properties:
                status:
                  type: string
                  default: success
                message:
                  type: string
                  default: File uploaded.
          400:
            description: Error
            schema:
              id: Error
              properties:
                status:
                  type: string
                  default: fail
                message:
                  type: string
                  default: Extension of file not allowed
        """
