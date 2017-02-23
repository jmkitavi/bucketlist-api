#! /usr/bin/env python
from flask_script import Manager
from app.config import Config
from flask_migrate import Migrate, MigrateCommand
from app import app, db


app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
