from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import sqlite3
import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///word.db'
db = SQLAlchemy(app)
Bootstrap(app)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(50), unique=True, nullable=False)
    chinese = db.Column(db.String(50), nullable=False)
    english_meaning = db.Column(db.String(200), nullable = True)
    date_added = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Word {self.english}>'
    
with app.app_context():
    db.create_all()
    
# conn = sqlite3.connect('word.db')
# c = conn.cursor()

# # 從japanese_characters table中選擇所需的欄位
# c.execute('SELECT hiragana_katakana, romaji FROM japanese1')

# # 將結果讀入一個list中
# characters = c.fetchall()
    
@app.route('/',methods=["GET", "POST"])
def home():
    with app.app_context():
        all_words = db.session.query(Word).all()
        total_words = db.session.query(Word).count()
    return render_template("home.html", words=all_words, total = total_words)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        #CREATE RECORD
        with app.app_context():
            new_word = Word(
                english = request.form['english'],
                chinese = request.form['chinese'],
                english_meaning = request.form['english_meaning'],
                date_added = datetime.datetime.now()
            )
            #f'{datetime.datetime.now().year}/{datetime.datetime.now().month}/{datetime.datetime.now().day}'
            db.session.add(new_word)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        words = Word.query.filter(Word.english.like(f'%{search_term}%') | Word.chinese.like(f'%{search_term}%') | Word.date_added.like(f'%{search_term}%')).all()
        return render_template('search.html', words=words, search_term=search_term)
    else:
        return render_template('search.html')
    
    
@app.route("/delete",methods=["GET", "POST"])
def delete():
    word_id = request.args.get('id')

    # DELETE A RECORD BY ID
    with app.app_context():
        word_to_delete = Word.query.get(word_id)
        db.session.delete(word_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    
@app.route('/edit', methods =["GET","POST"])
def edit():
    with app.app_context():
        if request.method == "POST":
            #UPDATE
            word_id = request.form["id"]
            word_to_update = Word.query.get(word_id)
            word_to_update.english = request.form["english"]
            word_to_update.chinese = request.form["chinese"]
            word_to_update.english_meaning = request.form["english_meaning"]
            word_to_update.date_added = datetime.datetime.now()
            db.session.commit()
            return redirect(url_for('home'))
        word_id = request.args.get('id')
        word_selected = Word.query.get(word_id)
    return render_template("edit_word.html",word = word_selected)
    

if __name__ == '__main__':
    app.run(debug=True,port=8000)