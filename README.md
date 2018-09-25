# hlts

## Setting up new hlts instance

via <https://devcenter.heroku.com/articles/heroku-cli>

make sure heroku CLI is insalled: <br>
`brew install heroku/brew/heroku`

login to heroku: <br>
`heroku login`

add postgres db: <br>
`heroku addons:add heroku-postgresql:hobby-dev --app [APPNAME]`

setup env variables: <br>
`heroku config:set FLASK_APP=run.py --app [APPNAME]` <br>
`heroku config:set DEFAULT_USER=[DEFAULT-USER] --app [APPNAME]` <br>
`heroku config:set DEFAULT_USER_PASSWORD=[DEFAULT-USER-PASSWORD] --app [APPNAME]` <br>
`heroku config:set DEFAULT_ADMIN=[DEFAULT-ADMIN] --app [APPNAME]` <br>
`heroku config:set DEFAULT_ADMIN_PASSWORD=[DEFAULT-ADMIN-PASSWORD] --app [APPNAME]` <br>
`heroku config:set SECRET_KEY=[SECRET_KEY] --app [APPNAME]` <br>

confirm config variables: <br>
`heroku config --app [APP NAME]`

remove config variable: <br>
`heroku config:unset [VARIABLE] --app [APPNAME]`

run cli command to initiate db: <br>
`heroku run flask init_db --app [APPNAME]`

basic structure to run cli commands: <br>
`heroku run flask [CLI-COMMAND] --app [APPNAME]`