import datetime
from mongoengine import connect, Document, StringField, BooleanField,ListField, DateTimeField, IntField
connect('paradigmatic', host='mongo', port=27017, username="paradigmatic", password="password", authentication_source='admin')


class User(Document):
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())
    email = StringField(required=True, max_length=100)
    first_name = StringField(max_length=200)
    last_name = StringField(max_length=200)
    hashed_password = StringField()
    user_type = StringField(default="student", choices=["admin", "superadmin", "staff", "student"])
    is_active = BooleanField(required=True, default=True)
    is_superuser = BooleanField(required=True, default=False)
    old_id = IntField(required=False)
    username = StringField(max_length=200, required=False)
    profile_pic = StringField(max_length=300)
