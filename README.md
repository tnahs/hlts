# hlts

## Setting up new hlts instance on Heroku

1. Install Heroku CLI: <br>
`brew install heroku/brew/heroku`

1. Login to Heroku: <br>
`heroku login`

2. Create new app: <br>
`heroku apps:create [APPNAME]`

3. Add Postgres DB: <br>
`heroku addons:add heroku-postgresql:hobby-dev --app [APPNAME]`

4. Setup env variables: <br>
`heroku config:set FLASK_APP=run.py --app [APPNAME]` <br>
`heroku config:set SECRET_KEY=[SECRET_KEY] --app [APPNAME]` <br>
`heroku config:set LOG_TO_STOUT=1 --app [APPNAME]` <br>
`heroku config:set MAIL_SERVER=[MAIL-SERVER] --app [APPNAME]` <br>
`heroku config:set MAIL_USERNAME=[MAIL-USERNAME] --app [APPNAME]` <br>
`heroku config:set MAIL_PASSWORD=[MAIL-PASSWORD] --app [APPNAME]` <br>
`heroku config:set MAIL_PORT=[MAIL-PORT] --app [APPNAME]` <br>
`heroku config:set MAIL_USE_TLS=[MAIL-USE-TLS] --app [APPNAME]` <br>
`heroku config:set DEFAULT_APP_USER=[DEFAULT-USER] --app [APPNAME]` <br>
`heroku config:set DEFAULT_APP_USER_PASSWORD=[DEFAULT-USER-PASSWORD] --app [APPNAME]` <br>
`heroku config:set ADMIN_APP_USER=[DEFAULT-ADMIN] --app [APPNAME]` <br>
`heroku config:set ADMIN_APP_USER_PASSWORD=[DEFAULT-ADMIN-PASSWORD] --app [APPNAME]` <br>

5. Connect app to Github.

6. Run cli command to initiate db/app: <br>
`heroku run flask init_db --app [APPNAME]`

---

```
Gmail settings via: http://flask.pocoo.org/snippets/85/
MAIL_SERVER='smtp.googlemail.com'
MAIL_PORT=587
MAIL_USE_TLS=1
```

---

To confirm config variables: <br>
`heroku config --app [APP NAME]`

To remove config variable: <br>
`heroku config:unset [VARIABLE] --app [APPNAME]`

Basic structure to run cli commands with flask/heroku: <br>
`heroku run flask [CLI-COMMAND] --app [APPNAME]`

To check heroku logs: <br>
`heroku logs --app [APPNAME]`

via <https://devcenter.heroku.com/articles/heroku-cli>