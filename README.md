---
languages:
  - Python
  - Flask API
products:
  - ping JWT Validation
  - oauth2
  - Flask API
  - azure App Service
  - azure FunctionApp
description: Python Library to validate Ping JWT token in Python/Flask API
urlFragment: 'https://github.com/arnabdeyusa/OAuth-Validation-Python'
---

# Step 1:
Create a .env file for local environment and set this following variable
ISSUER=Issuer_Link(e.g. https://bbbstage.cc.com)
AUDIENCE=appclientid
ALGO=algo(e.g. RS256)
AUTHURL=Validation_Key_Url(e.g. https://bbstage.cc.com/ext/regular)
Please make all these above variables are included in the Application Environment (e.g. DEV, STAGE, PROD)

| Key                                        | Value
| ------------------------------------------ | ------
| ISSUER                                     | Issuer_Link(e.g. https://bbbstage.cc.com)      
| AUDIENCE                                   | appclientid      
| ALGO                                       | algo(e.g. RS256)      
| AUTHURL                                    | Validation_Key_Url(e.g. https://bbbstage.cc.com/ext/regular)     

# Step 2:
Add the following as imports in the app.py file

```diff
from authvalidation import requires_auth
from authvalidation import AuthError
  ```
 
# Step 3:
Create the following function in your app.py (or the entry file to the APP) and attribute it with errorhandler as follows

```conf
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
  ```
  
# Step 4:
Wrap the endpoint of your app need to secure with the following attribute
@requires_auth, so the endpoint should look like as follows.

 ```conf
@app.route("/desc/<id>")
@requires_auth
def getdesc(id):
    obj.query = name
    results = obj.get_desc()
    return results[1].to_json()

  ```
