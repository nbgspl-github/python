import datetime

from mongoengine import Document, StringField, DateTimeField, FloatField


class Graph(Document):
    vis_id = StringField()
    name = StringField(max_length=50)
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=None)


class Node(Document):
    graph_id = StringField()
    vis_id = StringField()
    label = StringField(max_length=50)
    description = StringField()
    x = FloatField()
    y = FloatField()
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=None)


class Edge(Document):
    vis_id = StringField()
    source_id = StringField(required=True)
    destination_id = StringField(required=True)
    label = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=None)

