login_failed_response = {
    "description": "Fail authentication",
    "content": {
        "application/json": {
            "schema": {
                "id": "Fail authentication",
                "properties": {
                    "message": {
                        "type": "string",
                        "default": "User not found. | Provide a valid auth token. | Signature expired. Please log in again. | Invalid token. Please log in again.",
                    }
                },
            },
        }
    },
}
acces_denied_response = {
    "description": "Access denied.",
    "content": {
        "application/json": {
            "schema": {
                "id": "Access denied.",
                "properties": {
                    "message": {"type": "string", "default": "Access denied."}
                },
            },
        }
    },
}
