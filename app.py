from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
#import models
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(300), nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<notes %r>' % (self.nickname)


@app.route('/')
@app.route('/home')
def home():
    notes = Notes.query.order_by(Notes.date.desc()).all()
    return render_template('home.html', notes=notes)


@app.route('/post/<int:id>')
def post(id):
    note = Notes.query.get(id)
    return render_template('post.html', note=note)

@app.route('/post/<int:id>/del')
def note_delete(id):
    note = Notes.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/post/<int:id>/update', methods = ['POST', 'GET'])
def note_update(id):
    note = Notes.query.get(id)
    if request.method == "POST":
        note.title = request.form['title']
        note.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/home')
        except:
            return "При редактировании заметки произошла ошибка"

    else:
        return render_template('note_update.html', note=note)

@app.route('/create_note', methods = ['POST', 'GET'])
def create_note():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        note = Notes(title=title, text=text)

        try:
            db.session.add(note)
            db.session.commit()
            return redirect('/home')
        except:
            return "При добавлении заметки произошла ошибка"

    else:
        return render_template('create_note.html')


if __name__ == '__main__':
    app.run(debug=True)