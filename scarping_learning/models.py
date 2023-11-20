from datetime import datetime

from mongoengine import Document
from mongoengine.fields import StringField, IntField, DateTimeField, BooleanField, ReferenceField

SECTIONS = (("1", "Квартири"),
            ("2", "Аренда квартир"),
            ("3", "Дома"),
            ("4", "Аренда домiв"))


class User(Document):
    user_id = IntField(required=True)
    user_name = StringField(default=None)
    first_name = StringField(default=None)
    last_name = StringField(default=None)
    join_date = DateTimeField(default=datetime.now())
    is_admin = BooleanField(default=False)
    is_activated = BooleanField(default=False)


class City(Document):
    city_id = IntField(required=True)
    city_name = StringField(required=True)


class Notice(Document):
    notice_id = IntField(required=True)
    image_url = StringField(default=None)
    description = StringField(default=None)
    price = StringField(default=None)
    address = StringField(default=None)
    full_address = StringField(default=None)
    properties = StringField(default=None)


class Settings(Document):
    user = ReferenceField(User, required=True)
    city = ReferenceField(City, required=True)
    section = StringField(default="1", choices=SECTIONS)
