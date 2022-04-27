from app import db
from datetime import datetime

class notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(300), nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<notes %r>' % (self.nickname)