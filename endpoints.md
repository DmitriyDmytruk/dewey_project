---
description: >-
  You can see all endpoints descriptions, example of requests and responses on
  the /docs/ui/ or /redoc/
---

# Endpoints

* **/** - base endpoint \(for react ssr\)
* **/api/v1/celery/&lt;task\_id&gt;** - checks status of celery task \(import files\)
* **/api/v1/articles** - articles CRUD
* **/api/v1/articles/article/&lt;article\_id&gt;/to-pdf** - generating article pdf
* **/api/v1/articles/catalog/add/&lt;article\_id&gt;** - add article to catalog
* **/api/v1/articles/catalog/article/&lt;article\_id&gt;/delete** - delete article from catalog
* **/api​/v1​/articles​/my-catalog** - retrieve to catalog for current user
* **/api/v1/articles/search** - search articles. If `is_initial=True` forming usable states, tags, categories for selects
* **/api/v1/auth/login**
* **/api/v1/auth/logout**
* **/api/v1/auth/token-refresh**
* **/api/v1/articles/search-list/to-xls** - articles seach list to .xls
* **/api/v1/articles/search/api-user** - search articles \(api user\)
* **​/api​/v1​/articles​/to-xls** - all articles list to .xls
* **/api/v1/articles/upload** - upload articles \(csv, xls, xlsx, gsheet\). We generate errors file and send it to email, if importing file exists errors articles
* **/api/v1/articles/catalog/article/&lt;article\_id&gt;note/add** - note create
* **​/api​/v1​/articles​/categories** - retrieve all categories
* **​/api​/v1​/articles​/tags** - retrieve all tags
* **/api/v1/users/\(delete\|update\|create \(by admin\)\|&lt;user\_id&gt;\)** - users CRUD
* **​/api​/v1​/users​/my-profile** - profile retrieve
* **/api/v1/users/forgot-password** - forgot password request
* **/api/v1/users/profile/change-password** - change password
* **/api/v1/users/resetting-password** - reset password
* **/api/v1/users/set-password** - set password after registration
* **​/api​/v1​/users​/permissions** - retrieve all permissions
* **/api/v1/users/role\(-s\)** - roles CRUD

