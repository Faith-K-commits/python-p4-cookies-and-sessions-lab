#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0) + 1
    
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401
    
    article = Article.query.filter_by(id=id).first()
    if article:
        return jsonify(article.to_dict())  # Assuming Article model has a to_dict method
    else:
        return jsonify({"error": "Article not found"}), 404
    

if __name__ == '__main__':
    app.run(port=5555)
