#!flask/bin/python

import sys
import click
from os import getenv, path

from app import db
from app.models import User, Annotation

from flask import json, current_app
from sqlalchemy.exc import IntegrityError


def register_cli(app):

    @app.cli.command()
    def commands():
        click.echo(" \
            \n All available commands: \
            \n -------------------------------------------------------- \
            \n - init_db             Create all tables. \
            \n - drop_db             Drop all tables. \
            \n - create_user         Create single user. \
            \n - delete_user         Delete single user. \
            \n - edit_user           Edit single user. \
            \n - reset_users         Erase annoataions. \
            \n - erase_annotations   Erase users & re-create users. \
            \n - reset_all           Drop databases & re-create users.\
            \n -------------------------------------------------------- \
            \n ")

    def run_init_db():

        try:
            db.create_all()
            click.echo("Database initiated!")

        except:
            click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

    def run_drop_db():

        if click.confirm("\nWARNING! Drop all databases?", abort=True):

            try:
                db.drop_all()
                click.echo("Database erased!")

            except:
                click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

    def run_create_users():

        # Create default user
        user = User(username=getenv("DEFAULT_APPUSER_USERNAME"),
                    email=getenv("DEFAULT_APPUSER_EMAIL"),
                    admin=False)
        user.set_password(getenv("DEFAULT_APPUSER_PASSWORD"))

        try:
            db.session.add(user)
            db.session.commit()

        except:
            click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

        else:
            click.echo("\nCreated Default User!")
            click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

        # Create admin user
        user = User(username=getenv("ADMIN_APPUSER_USERNAME"),
                    email=getenv("ADMIN_APPUSER_EMAIL"),
                    admin=True)
        user.set_password(getenv("ADMIN_APPUSER_PASSWORD"))

        try:
            db.session.add(user)
            db.session.commit()

        except:
            click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

        else:
            click.echo("\nCreated Admin User!")
            click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

    @app.cli.command()
    def init_db():
        run_init_db()

    @app.cli.command()
    def drop_db():
        run_drop_db()

    @app.cli.command()
    def create_user():

        click.echo("\nCreate user...")

        username = click.prompt("Username")
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
        admin = click.prompt("Admin?", type=bool, default=False)

        user = User(username=username, admin=admin)
        user.set_password(password)

        db.session.add(user)

        try:
            db.session.commit()

        except IntegrityError:
            click.echo("Username already taken!")

        except:
            click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

        else:
            click.echo("\nCreated User!")
            click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

    @app.cli.command()
    def delete_user():

        click.echo("\nDelete user...")

        username = click.prompt("Username")

        user = User.query.filter_by(username=username).first()

        if user and click.confirm("User exists! Delete user?", abort=True):

            db.session.delete(user)

            try:
                db.session.commit()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nDeleted user!")

        else:

            click.echo("User does not exist!")

    @app.cli.command()
    def edit_user():

        click.echo("\nEdit User...")

        username = click.prompt("Username")

        user = User.query.filter_by(username=username).first()

        if user and click.confirm("User exists! Edit user?", abort=True):

            if click.confirm("Change Username?"):
                new_username = click.prompt("New Username")
                user.username = new_username

            if click.confirm("Change Email?"):
                new_email = click.prompt("New Email")
                user.email = new_email

            if click.confirm("Change Password?"):
                new_password = click.prompt("New Password", hide_input=True, confirmation_prompt=True)
                user.set_password(new_password)

            if click.confirm("Change Admin Status?"):
                new_admin_status = click.prompt("New Admin Status?", type=bool)
                user.admin = new_admin_status

            try:
                db.session.commit()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nUpdated User!")
                click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

        else:

            click.echo("User does not exist!")

    @app.cli.command()
    def reset_users():

        if click.confirm("\nWARNING! Reset users to default?", abort=True):

            click.echo("\nResetting users...")

            # Remove all users
            try:
                User.query.delete()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nRemoved all users!")

            # Create users
            run_create_users()

    @app.cli.command()
    def erase_annotations():

        if click.confirm("\nWARNING! Reset annotations?", abort=True):

            click.echo("\nResetting annotations...")

            # Remove all annotations
            try:
                Annotation.query.delete()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nRemoved all users!")

    @app.cli.command()
    def reset_all():

        if click.confirm("\nWARNING! Perform full reset?", abort=True):

            click.echo("\nPerforming full reset...")

            # Drop DBs
            run_drop_db()

            # Create DBs
            run_init_db()

            # Create users
            run_create_users()

    @app.cli.command()
    def init_welcome():

        click.echo("\nAdding welcome annotations...")

        welcome_json = path.join(current_app.root_path, "init_data", "welcome.json")

        with open(welcome_json) as f:
            welcome_annotations = json.load(f)

        for annotation in welcome_annotations:

            importing = Annotation()
            importing.deserialize(annotation)

            db.session.add(importing)

        db.session.commit()
