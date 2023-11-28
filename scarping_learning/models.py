from datetime import datetime

import mongoengine
from mongoengine import Document
from mongoengine.fields import (
    StringField,
    IntField,
    DateTimeField,
    BooleanField,
    ReferenceField,
)


class User(Document):
    user_id = IntField(required=True)
    user_name = StringField(default=None)
    first_name = StringField(default=None)
    last_name = StringField(default=None)
    join_date = DateTimeField(default=datetime.now)
    is_admin = BooleanField(default=False)
    is_activated = BooleanField(default=False)


class City(Document):
    city_id = IntField(required=True)
    city_name = StringField(required=True)


class Notice(Document):
    notice_id = IntField(required=True)
    image_url = StringField(default=None)
    description = StringField(default=None)
    price = IntField(default=None)
    address = StringField(default=None)
    full_address = StringField(default=None)
    properties = StringField(default=None)
    city = ReferenceField(City, required=True)
    creation_date = DateTimeField(default=datetime.utcnow)


class Section(Document):
    section_id = IntField(required=True)
    section_title = StringField(default="")


class Setting(Document):
    user = ReferenceField(
        User, required=True, reverse_delete_rule=mongoengine.DO_NOTHING
    )
    city = ReferenceField(
        City, required=True, reverse_delete_rule=mongoengine.DO_NOTHING
    )
    section = ReferenceField(
        Section, required=True, reverse_delete_rule=mongoengine.DO_NOTHING
    )
