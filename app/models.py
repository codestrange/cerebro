from flask_mongoengine import MongoEngine

db = MongoEngine()


class Message(db.Document):
    text = db.StringField()
    tags = db.ListField(db.StringField())

    def __str__(self):
        return str({'id': self.id, 'text': self.text, 'tags': self.tags})
