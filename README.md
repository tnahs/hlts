# hlts

### Annotation Schema

``` json
{
    "id": string,
    "passage": string,
    "notes": string,
    "source": {
        "name": string,
        "author": string
    },
    "tags": list,
    "collections": list,
    "created": date,
    "modified": date,
    "origin": string,
    "protected": bool,
    "deleted": bool
}
```
Dates as ISO 8601 format.

<br>

### Setting up new hlts instance on Heroku

1. Install Heroku CLI:
<br> `brew install heroku/brew/heroku`

2. run `init_new_herokuapp.sh`

3. At <https://dashboard.heroku.com/apps/{APPNAME}> Connect app to `hlts` repo.

4. Run `init_db` initiate db/app:
<br> `heroku run flask init_db --app {APPNAME}`

---

To confirm config variables:
<br> `heroku config --app {APP NAME}`

To remove config variable:
<br> `heroku config:unset {VARIABLE} --app {APPNAME}`

Basic structure to run cli commands with flask/heroku:
<br> `heroku run flask {CLI-COMMAND} --app {APPNAME}`

To check heroku logs:
<br> `heroku logs --app {APPNAME}`

via <https://devcenter.heroku.com/articles/heroku-cli>

---

``` s
# Gmail settings via: http://flask.pocoo.org/snippets/85/
MAIL_SERVER='smtp.googlemail.com'
MAIL_PORT=587
MAIL_USE_TLS=1
```

---