from flask_mongoengine import MongoEngine

db = MongoEngine()

class Message(db.Document):
    text = db.StringField()
    tags = db.ListField(db.StringField())
