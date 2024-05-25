from pony.orm import Database, PrimaryKey, Required, \
    db_session, Set
from os import getenv
from datetime import datetime


db = Database()
db.bind(provider='sqlite', filename=f'{"/app/config/" if getenv("IS_DOCKER", False) else "./"}/database.sqlite',
        create_db=True)


class Posts(db.Entity):
    id = PrimaryKey(str, 255)
    url = Required(str, 255)


class Subscriptions(db.Entity):
    telegram_id = Required(int, size=64)


db.generate_mapping(create_tables=True)
