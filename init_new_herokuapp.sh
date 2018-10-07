#!/bin/bash

# Initiate and configure new hlts instance on Heroku.com

# Default variables for hlts
FLASK_APP="run.py"
SECRET_KEY=$(openssl rand -base64 32)
LOGGING_TO_STOUT="1"

DEFAULT_LOGGING_MAIL_SERVER="smtp.googlemail.com"
DEFAULT_LOGGING_MAIL_USERNAME="hlts.logging@gmail.com"
DEFAULT_LOGGING_MAIL_PORT="587"
DEFAULT_LOGGING_MAIL_TLS="1"

echo
echo "Accessing Heroku Login..."
echo

# Login
heroku login

if [ $? -eq 0 ]; then

    echo
    echo "Enter new app config..."
    echo

    # Gather new app settings
    read -p "App Name: " APP_NAME
    read -p "Default User Username: " DEFAULT_APPUSER_USERNAME
    read -p "Default User E-mail: " DEFAULT_APPUSER_EMAIL
    read -p "Default User Password: " DEFAULT_APPUSER_PASSWORD
    read -p "Admin User Username: " ADMIN_APPUSER_USERNAME
    read -p "Admin User E-mail: " ADMIN_APPUSER_EMAIL
    read -p "Admin User Password: " -i ADMIN_APPUSER_PASSWORD
    read -e -p "Logging Mail Server: " -i $DEFAULT_LOGGING_MAIL_SERVER LOGGING_MAIL_SERVER
    read -e -p "Logging Mail Username: " -i $DEFAULT_LOGGING_MAIL_USERNAME LOGGING_MAIL_USERNAME
    read -p "Logging Mail Password: " LOGGING_MAIL_PASSWORD
    read -e -p "Logging Mail Port: " -i $DEFAULT_LOGGING_MAIL_PORT LOGGING_MAIL_PORT
    read -e -p "Logging Mail TLS?: " -i $DEFAULT_LOGGING_MAIL_TLS  LOGGING_MAIL_TLS

    echo
    echo "Creating new Heroku app..."
    echo

    # Create new app
    heroku apps:create $APP_NAME

    echo
    echo "Adding Postgress to app..."
    echo

    # Add Postgres DB
    heroku addons:add heroku-postgresql:hobby-dev --app $APP_NAME

    echo
    echo "Setting config variables"
    echo

    # Setup config variables
    heroku config:set \
        FLASK_APP=$FLASK_APP \
        SECRET_KEY=$SECRET_KEY \
        LOGGING_TO_STOUT=$LOGGING_TO_STOUT \
        LOGGING_MAIL_SERVER=$LOGGING_MAIL_SERVER \
        LOGGING_MAIL_USERNAME=$LOGGING_MAIL_USERNAME \
        LOGGING_MAIL_PASSWORD=$LOGGING_MAIL_PASSWORD \
        LOGGING_MAIL_PORT=$LOGGING_MAIL_PORT \
        LOGGING_MAIL_TLS=$LOGGING_MAIL_TLS \
        DEFAULT_APPUSER_USERNAME=$DEFAULT_APPUSER_USERNAME \
        DEFAULT_APPUSER_EMAIL=$DEFAULT_APPUSER_EMAIL \
        DEFAULT_APPUSER_PASSWORD=$DEFAULT_APPUSER_PASSWORD \
        ADMIN_APPUSER_USERNAME=$ADMIN_APPUSER_USERNAME \
        ADMIN_APPUSER_EMAIL=$ADMIN_APPUSER_EMAIL \
        ADMIN_APPUSER_PASSWORD=$ADMIN_APPUSER_PASSWORD \
        --app $APP_NAME
else

    echo
    echo "Invalid Herko Credentials!"
    echo "Exiting!"
    exit 1
fi