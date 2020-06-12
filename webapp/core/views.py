from flask import render_template


def index():
    """Base endpoint
    ---
    responses:
      200:
        description: receives `index.html`
        content:
          application/json:
            schema:
              type: string
    """
    return render_template("core/index.html")
