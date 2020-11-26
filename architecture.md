---
description: Maine items of the project design
---

# Architecture



```text
file-upload/
kubernetes/
migrations/
webapp/
    articles/
    auth/
    core/
    static/
    users/
    utils/
    __init__.py
.isort.cfg
.pylintrc
main.py
manage.py
pyproject.toml
stylecheckerrunner.sh
```

* **file-upload** - directory for imported files
* **kubernetes** - k8s settings
* **migrations** - all migrations
* **.isort.cfg** - ****isort config
* **.pylintrc** - ****pylint config
* **pyproject.toml** - ****black config
* **main.py** - start point for run application
* **manage.py** - script for creating fixture \(see `webapp/fixtures`\)
* **stylecheckerrunner** - ****sh script for run stylechecker \(`isort`, `black`, `pylint`\)

## webapp/ \(main application\)

* **articles** - articles bp - Articles CRUD, search, import/export \(csv, xls, xlsx, gsheet\)
* **auth** - auth \(login/logout, token refresh\) methods
* **core** - common, base logic
* **users** - Users, Roles and Permissions logic
* **utils** - common files \(`fixtures` , `mailing`, `decorators` etc\)
* **static** - build static from front-end
* **\_\_init\_\_.py** - creates instance of application

{% hint style="info" %}
Each blueprint is, if possible, divided into different services for a clean architecture
{% endhint %}

