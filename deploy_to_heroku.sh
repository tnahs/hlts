#!/bin/bash

# Setup and configure new HLTS app on Heroku.com

# Default variables for HLTS
FLASK_APP="run.py"
SECRET_KEY=$(openssl rand -base64 32)
LOGGING_TO_STOUT="True"

DEFAULT_APP_DOMAIN_URL="hlts.app"
DEFAULT_APP_SUBDOMAIN_NAME="www"

DEFAULT_LOGGING_MAIL_SERVER="smtp.googlemail.com"
DEFAULT_LOGGING_MAIL_USERNAME="hltsapp.logs@gmail.com"
DEFAULT_LOGGING_MAIL_PORT="587"
DEFAULT_LOGGING_MAIL_USE_TLS="True"

DEFAULT_MAIL_SERVER="smtp.googlemail.com"
DEFAULT_MAIL_USERNAME="hltsapp.mail@gmail.com"
DEFAULT_MAIL_PORT="587"
DEFAULT_MAIL_USE_TLS="True"
DEFAULT_MAIL_USE_SSL="False"

echo
echo "Accessing Heroku Login..."
echo

# Login
heroku login

if [ $? -eq 0 ]; then

    echo
    echo "Configure new Heroku app..."
    echo

    # Gather new app settings
    read -p    "App Name: " APP_NAME
    read -e -p "App Domain Url: " -i $DEFAULT_APP_DOMAIN_URL APP_DOMAIN_URL
    read -e -p "App Subdomaine: " -i $DEFAULT_APP_SUBDOMAIN_NAME APP_SUBDOMAIN_NAME

    read -p    "Default User Username (4-32 characters): " DEFAULT_APPUSER_USERNAME
    read -p    "Default User E-mail: " DEFAULT_APPUSER_EMAIL
    read -p    "Default User Password (6-32 characters): " DEFAULT_APPUSER_PASSWORD
    read -p    "Admin User Username (4-32 characters): " ADMIN_APPUSER_USERNAME
    read -p    "Admin User E-mail: " ADMIN_APPUSER_EMAIL
    read -p    "Admin User Password (6-32 characters): " ADMIN_APPUSER_PASSWORD

    read -e -p "Logging Mail Server: " -i $DEFAULT_LOGGING_MAIL_SERVER LOGGING_MAIL_SERVER
    read -e -p "Logging Mail Username: " -i $DEFAULT_LOGGING_MAIL_USERNAME LOGGING_MAIL_USERNAME
    read -p    "Logging Mail Password: " LOGGING_MAIL_PASSWORD
    read -e -p "Logging Mail Port: " -i $DEFAULT_LOGGING_MAIL_PORT LOGGING_MAIL_PORT
    read -e -p "Logging Mail Use TLS?: " -i $DEFAULT_LOGGING_MAIL_USE_TLS  LOGGING_MAIL_USE_TLS

    read -e -p "Mail Server: " -i $DEFAULT_MAIL_SERVER MAIL_SERVER
    read -e -p "Mail Username: " -i $DEFAULT_MAIL_USERNAME MAIL_USERNAME
    read -p    "Mail Password: " MAIL_PASSWORD
    read -e -p "Mail Port: " -i $DEFAULT_MAIL_PORT MAIL_PORT
    read -e -p "Mail Use TLS?: " -i $DEFAULT_MAIL_USE_TLS MAIL_USE_TLS
    read -e -p "Mail Use SSL?: " -i $DEFAULT_MAIL_USE_SSL MAIL_USE_SSL

    echo
    echo "Creating new Heroku app..."
    echo

    # Create new app
    heroku apps:create $APP_NAME

    echo
    echo "Adding Postgress..."
    echo

    # Add Postgres DB
    heroku addons:add heroku-postgresql:hobby-dev --app $APP_NAME

    echo
    echo "Setting subdomain to $APP_SUBDOMAIN_NAME.$APP_DOMAIN_URL..."
    echo

    # Add subdomain
    heroku domains:add $APP_SUBDOMAIN_NAME.$APP_DOMAIN_URL --app $APP_NAME

    echo
    echo "Setting config variables..."
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
        LOGGING_MAIL_USE_TLS=$LOGGING_MAIL_USE_TLS \
        MAIL_SERVER=$MAIL_SERVER \
        MAIL_USERNAME=$MAIL_USERNAME \
        MAIL_PASSWORD=$MAIL_PASSWORD \
        MAIL_PORT=$MAIL_PORT \
        MAIL_USE_TLS=$MAIL_USE_TLS \
        MAIL_USE_SSL=$MAIL_USE_SSL \
        DEFAULT_APPUSER_USERNAME=$DEFAULT_APPUSER_USERNAME \
        DEFAULT_APPUSER_EMAIL=$DEFAULT_APPUSER_EMAIL \
        DEFAULT_APPUSER_PASSWORD=$DEFAULT_APPUSER_PASSWORD \
        ADMIN_APPUSER_USERNAME=$ADMIN_APPUSER_USERNAME \
        ADMIN_APPUSER_EMAIL=$ADMIN_APPUSER_EMAIL \
        ADMIN_APPUSER_PASSWORD=$ADMIN_APPUSER_PASSWORD \
        --app $APP_NAME

    # Echo subdomain info
    heroku domains --app $APP_NAME

    echo
    echo "Next Steps:"
    echo "1. Connect $APP_NAME to HLTS repo."
    echo "2. Initialize Database and HLTS Beta:"
    echo "   ----------------------------------"
    echo "   heroku run flask db upgrade --app $APP_NAME"
    echo "   heroku run flask init_beta --app $APP_NAME"
    echo "   ----------------------------------"
    echo "3. Configure $APP_NAME's DNS provider to point to the DNS Target."
    echo

else

    echo
    echo "Invalid Herko Credentials!"
    echo "Exiting!"
    exit 1
fi