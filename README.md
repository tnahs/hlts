# hlts

## Setting up new hlts instance on Heroku

1. Install Heroku CLI:
<br> `brew install heroku/brew/heroku`

2. Login to Heroku:
<br> `heroku login`

3. Create new app:
<br> `heroku apps:create {APPNAME}`

4. Add Postgres DB:
<br> `heroku addons:add heroku-postgresql:hobby-dev --app {APPNAME}`

5. Setup env variables:
<br> `heroku config:set FLASK_APP=run.py --app {APPNAME}`
<br> `heroku config:set SECRET_KEY={SECRET_KEY} --app {APPNAME}`
<br>
<br> `heroku config:set LOGGING_TO_STOUT=1 --app {APPNAME}`
<br> `heroku config:set LOGGING_MAIL_SERVER={LOGGING-MAIL-SERVER} --app {APPNAME}`
<br> `heroku config:set LOGGING_MAIL_USERNAME={LOGGING-MAIL-USERNAME} --app {APPNAME}`
<br> `heroku config:set LOGGING_MAIL_PASSWORD={LOGGING-MAIL-PASSWORD} --app {APPNAME}`
<br> `heroku config:set LOGGING_MAIL_PORT={LOGGING-MAIL-PORT} --app {APPNAME}`
<br> `heroku config:set LOGGING_MAIL_USE_TLS={LOGGING-MAIL-USE-TLS} --app {APPNAME}`
<br>
<br> `heroku config:set DEFAULT_APP_USER={DEFAULT-USER} --app {APPNAME}`
<br> `heroku config:set DEFAULT_APP_USER_PASSWORD={DEFAULT-USER-PASSWORD} --app {APPNAME}`
<br> `heroku config:set ADMIN_APP_USER={DEFAULT-ADMIN} --app {APPNAME}`
<br> `heroku config:set ADMIN_APP_USER_PASSWORD={DEFAULT-ADMIN-PASSWORD} --app {APPNAME}`

1. Connect app to `hlts` repo.

2. Run `init_db` initiate db/app:
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

```
Gmail settings via: http://flask.pocoo.org/snippets/85/
MAIL_SERVER='smtp.googlemail.com'
MAIL_PORT=587
MAIL_USE_TLS=1
```

---