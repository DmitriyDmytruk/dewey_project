from flask import render_template


def index():
    """
    Base endpoint
    """
    return render_template("core/index.html")
