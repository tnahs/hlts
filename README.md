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
```
heroku config:set
    FLASK_APP={FLASK_APP} \
    SECRET_KEY={SECRET_KEY} \
    LOGGING_TO_STOUT={LOGGING_TO_STOUT} \
    LOGGING_MAIL_SERVER={LOGGING_MAIL_SERVER} \
    LOGGING_MAIL_USERNAME={LOGGING_MAIL_USERNAME} \
    LOGGING_MAIL_PASSWORD={LOGGING_MAIL_PASSWORD} \
    LOGGING_MAIL_PORT={LOGGING_MAIL_PORT} \
    LOGGING_MAIL_USE_TLS={LOGGING_MAIL_USE_TLS} \
    DEFAULT_APPUSER_USERNAME={DEFAULT_APPUSER_USERNAME} \
    DEFAULT_APPUSER_EMAIL={DEFAULT_APPUSER_EMAIL} \
    DEFAULT_APPUSER_PASSWORD={DEFAULT_APPUSER_PASSWORD} \
    ADMIN_APPUSER_USERNAME={ADMIN_APPUSER_USERNAME
    ADMIN_APPUSER_EMAIL={ADMIN_APPUSER_EMAIL} \
    ADMIN_APPUSER_PASSWORD={ADMIN_APPUSER_PASSWORD} \
    --app {APPNAME}
```

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