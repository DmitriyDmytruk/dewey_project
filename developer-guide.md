---
description: Instructions for developer
---

# Developer guide

## Development

* to run the project:

```bash
flask db migrate && flask run
```

* to run tests

```bash
python -m pytest
```

* to run celery

```bash
celery -A webapp.runcelery:celery worker -l info
```

* for import from google sheet - to set environment variable `GSHEETS_CREDENTIALS_JSON` \(see `gsheet-creds.json`\) and run celery
* in `__init__.py` must be:



  ```text
  app.elasticsearch = (
      Elasticsearch([app.config["ELASTICSEARCH_URL"]])
      if app.config["ELASTICSEARCH_URL"]
      else None
  )
  ```



