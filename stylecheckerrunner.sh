#!/usr/bin/env bash
isort
black . --diff
pylint --load-plugins pylint_flask_sqlalchemy webapp/