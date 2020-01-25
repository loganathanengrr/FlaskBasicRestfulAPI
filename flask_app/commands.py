import click
from flask.cli import with_appcontext

from .extensions import db

@click.command(name='create_tables')
@with_appcontext
def create_tables():
	try:
		db.create_all()
		return 'Created'
	except Exception as e:
		raise