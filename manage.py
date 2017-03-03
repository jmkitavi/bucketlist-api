#! /usr/bin/env python
import os
from random import randint
from flask_script import Manager
from app.config import Config
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from faker import Faker
from app.models import *

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

fake = Faker()


@manager.command
def seed():
    """
    Populates the database with dummy records
    """
    print('seeding...')
    users = []
    bucketlists = []
    bucketlist_items = []

    # create 10 users
    print('\tCreating users...')
    for i in range(10):
        users.append(Users(fake.first_name(), password='password'))
    db.session.bulk_save_objects(users)
    db.session.commit()
    print('\tCreating users complete!')

    # create BucketLists
    countries = []
    for i in range(100):
        countries.append(fake.country())
    bucketlists = [BucketList(title=country, created_by=randint(1, 9))
                   for country in set(countries)]
    db.session.bulk_save_objects(bucketlists)
    db.session.commit()
    print('\tCreating bucketlist items complete!')

    # create BucketListItem
    names = []
    for i in range(100):
        names.append(fake.name())
    bucketlist_items = [BucketListItems(
        item_name=name, bucketlist_id=randint(55, 139)) for name in set(names)]
    db.session.bulk_save_objects(bucketlist_items)
    db.session.commit()
    print('\tCreating bucketlist items complete!')
    print('Seeding complete!')

if __name__ == '__main__':
    manager.run()
