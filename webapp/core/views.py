from flask import render_template


def index():
    """Base endpoint
    ---
    responses:
      200:
        description: receives `index.html`
    """
    return render_template("core/index.html")
