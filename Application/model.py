from bson.objectid import ObjectId
from mongoengine import *
import datetime

class User(Document):
    email = StringField(required=True,unique=True)
    first_name = StringField(max_length=50,required=True)
    last_name = StringField(max_length=50,required=True)
    handle = StringField(max_length=50,required=True)
    password = StringField(max_length=50,required=True)

class Blog(Document):
    title = StringField(max_length=120, required=True)
    summary = StringField(max_length=1000, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    like = IntField(default=0)
    dislike = IntField(default=0)
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)
    authorhandle = StringField()
    commentcount = IntField(default=0)
    meta = {'allow_inheritance': True}

class Comment(Document):
    content = StringField()
    author = ReferenceField(User)
    blog = ReferenceField(Blog, reverse_delete_rule=CASCADE)
    like = IntField(default=0)
    dislike = IntField(default=0)
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)
    authorhandle = StringField()
    meta = {'allow_inheritance': True}

class Reply(Document):
    content = StringField()
    author = ReferenceField(User)
    comment = ReferenceField(Comment, reverse_delete_rule=CASCADE)
    like = IntField(default=0)
    dislike = IntField(default=0)
    created = DateTimeField(default=datetime.datetime.utcnow)
    modified = DateTimeField(default=datetime.datetime.utcnow)
    authorhandle = StringField()

class TextPost(Blog):
    content = StringField()

