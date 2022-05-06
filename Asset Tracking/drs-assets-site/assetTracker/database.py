from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Test stuff not sure if needed
#Will check later but not sure.
#Probably need the imported stuff but not the commands. 
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
#Test stuff ends here

engine = create_engine('sqlite:///instance/assetTracker.sqlite')
db_sessionmaker = sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine)
db_session = scoped_session(db_sessionmaker)

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import assetTracker.models
    Base.metadata.create_all(bind=engine)
    
def build_test():
    from assetTracker.dbCommands import constructTestObjects
    constructTestObjects(db_session)
    
def print_all_objects():
    from assetTracker.dbCommands import printAll
    printAll(db_session)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(build_test_command)
    app.cli.add_command(print_all_objects_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    
@click.command('build-test')
@with_appcontext
def build_test_command():
    """Attempt to add test objects to database performed."""
    build_test()
    click.echo('Attempted to add test objects to database performed.')
    
@click.command('print-all-objects')
@with_appcontext
def print_all_objects_command():
    """Attempt to print all objects"""
    click.echo('Printing all objects.')
    print_all_objects()
    #Areas are currently being returned as cursor objects,
    #Also the readers don't have valid area ids so that's probably borked