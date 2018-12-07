#!/bin/bash

###############################################################################
###############################################################################
# Setup and configure new HLTS app on Heroku.com
###############################################################################
###############################################################################


###############################################################################
# Default variables for HLTS on Heroku
###############################################################################

FLASK_APP="run.py"
SECRET_KEY=$(openssl rand -base64 32)
LOGGING_TO_STOUT="True"

###############################################################################
# Enviromnet variables visible here must be set for script to run properly.
###############################################################################

DEFAULT_APP_DOMAIN_URL=$ENV_APP_DOMAIN_URL
DEFAULT_APP_SUBDOMAIN_NAME=$ENV_APP_SUBDOMAIN_NAME

DEFAULT_ADMIN_USERNAME=$ENV_ADMIN_USERNAME
DEFAULT_ADMIN_EMAIL=$ENV_ADMIN_EMAIL
DEFAULT_ADMIN_PASSWORD=$ENV_ADMIN_PASSWORD

DEFAULT_LOGGING_MAIL_SERVER=$ENV_LOGGING_MAIL_SERVER
DEFAULT_LOGGING_MAIL_USERNAME=$ENV_LOGGING_MAIL_USERNAME
DEFAULT_LOGGING_MAIL_PASSWORD=$ENV_LOGGING_MAIL_PASSWORD
DEFAULT_LOGGING_MAIL_PORT=$ENV_LOGGING_MAIL_PORT
DEFAULT_LOGGING_MAIL_USE_TLS=$ENV_LOGGING_MAIL_USE_TLS

DEFAULT_MAIL_SERVER=$ENV_MAIL_SERVER
DEFAULT_MAIL_USERNAME=$ENV_MAIL_USERNAME
DEFAULT_MAIL_PASSWORD=$ENV_MAIL_PASSWORD
DEFAULT_MAIL_PORT=$ENV_MAIL_PORT
DEFAULT_MAIL_USE_TLS=$ENV_MAIL_USE_TLS
DEFAULT_MAIL_USE_SSL=$ENV_MAIL_USE_SSL

###############################################################################

function deploy_herokuapp {

    echo
    echo "Configure new Heroku app..."
    echo

    # Gather new app settings
    read    -p "App Name: "                    APP_NAME
    read -e -p "App Domain URL: "           -i $DEFAULT_APP_DOMAIN_URL APP_DOMAIN_URL
    read    -p "App Subdomain: "               APP_SUBDOMAIN_NAME

    read    -p "Username (4-32): "             USER_USERNAME
    read    -p "E-mail: "                      USER_EMAIL
    read    -p "Password (6-32): "             USER_PASSWORD
    read -e -p "Admin Username (4-32): "    -i $DEFAULT_ADMIN_USERNAME ADMIN_USERNAME
    read -e -p "Admin E-mail: "             -i $DEFAULT_ADMIN_EMAIL ADMIN_EMAIL
    read -e -p "Admin Password (6-32): "    -i $DEFAULT_ADMIN_PASSWORD ADMIN_PASSWORD

    read -e -p "Logging Mail Server: "      -i $DEFAULT_LOGGING_MAIL_SERVER LOGGING_MAIL_SERVER
    read -e -p "Logging Mail Username: "    -i $DEFAULT_LOGGING_MAIL_USERNAME LOGGING_MAIL_USERNAME
    read -e -p "Logging Mail Password: "    -i $DEFAULT_LOGGING_MAIL_PASSWORD LOGGING_MAIL_PASSWORD
    read -e -p "Logging Mail Port: "        -i $DEFAULT_LOGGING_MAIL_PORT LOGGING_MAIL_PORT
    read -e -p "Logging Mail Use TLS?: "    -i $DEFAULT_LOGGING_MAIL_USE_TLS  LOGGING_MAIL_USE_TLS

    read -e -p "Mail Server: "              -i $DEFAULT_MAIL_SERVER MAIL_SERVER
    read -e -p "Mail Username: "            -i $DEFAULT_MAIL_USERNAME MAIL_USERNAME
    read -e -p "Mail Password: "            -i $DEFAULT_MAIL_PASSWORD MAIL_PASSWORD
    read -e -p "Mail Port: "                -i $DEFAULT_MAIL_PORT MAIL_PORT
    read -e -p "Mail Use TLS?: "            -i $DEFAULT_MAIL_USE_TLS MAIL_USE_TLS
    read -e -p "Mail Use SSL?: "            -i $DEFAULT_MAIL_USE_SSL MAIL_USE_SSL

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
        USER_USERNAME=$USER_USERNAME \
        USER_EMAIL=$USER_EMAIL \
        USER_PASSWORD=$USER_PASSWORD \
        ADMIN_USERNAME=$ADMIN_USERNAME \
        ADMIN_EMAIL=$ADMIN_EMAIL \
        ADMIN_PASSWORD=$ADMIN_PASSWORD \
        --app $APP_NAME

    # Echo subdomain info
    heroku domains --app $APP_NAME

    echo
    echo "Next Steps:"
    echo "1. Connect $APP_NAME to HLTS repo."
    echo "2. Initialize Database, User and Beta:"
    echo "   ----------------------------------"
    echo "   heroku run flask init_db --app $APP_NAME"
    echo "   heroku run flask create_app_user --app $APP_NAME"
    echo "   heroku run flask init_beta --app $APP_NAME"
    echo "   ----------------------------------"
    echo "3. Configure $APP_NAME's DNS provider to point to the DNS Target."
    echo "   NOTE: Don't forget to add a . after the DNS Target!"
    echo
}

###############################################################################

# Check if logged in
heroku auth:whoami

if [ $? -eq 0 ]; then

    deploy_herokuapp

else

    echo
    echo "Accessing Heroku Login..."
    echo

    # Login
    heroku login

    if [ $? -eq 0 ]; then

        deploy_herokuapp

    else

        echo
        echo "Invalid Herko Credentials!"
        echo "Exiting!"
        exit 1

    fi

fi