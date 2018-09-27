#!flask/bin/python

import sys
import click
from os import getenv

from app import db
from app.models import User
from sqlalchemy.exc import IntegrityError


def register_cli(app):

    @app.cli.command()
    def init_db():

        try:
            db.create_all()
            click.echo("Database Initiated!")

        except:
            click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

    @app.cli.command()
    def drop_db():

        if click.confirm("\nWARNING! Drop all databases?", abort=True):

            try:
                db.drop_all()
                click.echo("Database erased!")

            except:
                click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

    @app.cli.command()
    def create_user():

        click.echo("\nCreating User...")

        username = click.prompt("Username")
        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
        admin = click.prompt("Admin?", type=bool, default=False)

        user = User(username=username, password=password, admin=admin)

        try:
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            click.echo("Username already taken!")

        except:
            click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

        else:
            click.echo("\nCreated User!")
            click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

    @app.cli.command()
    def edit_user():

        click.echo("\nEditing User...")

        username = click.prompt("Username")

        user = User.query.filter_by(username=username).first()

        if click.confirm("Change Username?"):
            new_username = click.prompt("New Username")
            user.username = new_username

        if click.confirm("Change Password?"):
            new_password = click.prompt("New Password", hide_input=True, confirmation_prompt=True)
            user.password = user._hash_password(new_password)

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

    @app.cli.command()
    def revert_user():

        if click.confirm("\nWARNING! Reset users to default?", abort=True):

            click.echo("\nResetting users...")

            # Remove all users

            for user in User.query.all():
                db.session.delete(user)

            db.session.commit()

            # Create Default user

            user = User(username=getenv("DEFAULT_APP_USER"),
                        password=getenv("DEFAULT_APP_USER_PASSWORD"),
                        admin=False)

            try:
                db.session.add(user)
                db.session.commit()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nCreated Default User!")
                click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

            # Create Admin user

            user = User(username=getenv("ADMIN_APP_USER"),
                        password=getenv("ADMIN_APP_USER_PASSWORD"),
                        admin=True)

            try:
                db.session.add(user)
                db.session.commit()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nCreated Admin User!")
                click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

    @app.cli.command()
    def quick_reset():

        if click.confirm("\nWARNING! Perform quick reset?", abort=True):

            # Drop DBs

            try:
                db.drop_all()
                click.echo("Database Initiated!")

            except:
                click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

            # Create DBs

            try:
                db.create_all()
                click.echo("Database erased!")

            except:
                click.echo("Unexpected error: {0}".format(sys.exc_info()[0]))

            # Create Default user

            user = User(username=getenv("DEFAULT_APP_USER"),
                        password=getenv("DEFAULT_APP_USER_PASSWORD"),
                        admin=False)

            try:
                db.session.add(user)
                db.session.commit()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nCreated Default User!")
                click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))

            # Create Admin user

            user = User(username=getenv("ADMIN_APP_USER"),
                        password=getenv("ADMIN_APP_USER_PASSWORD"),
                        admin=True)

            try:
                db.session.add(user)
                db.session.commit()

            except:
                click.echo("Unexpected error: {0}.".format(sys.exc_info()[0]))

            else:
                click.echo("\nCreated Admin User!")
                click.echo("<Username: {0.username}> <Admin: {0.is_admin}>".format(user))
