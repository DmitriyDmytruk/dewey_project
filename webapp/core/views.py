from flask import Blueprint, render_template


base_blueprint = Blueprint("base", __name__, template_folder="templates")


@base_blueprint.route("/")
def index():
    """Base endpoint
    ---
    responses:
      200:
        description: receives `index.html`
    """
    return render_template("core/index.html")
