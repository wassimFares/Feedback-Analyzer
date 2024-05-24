from flask import Flask, render_template, request, jsonify
from model import comment_analysis
from scrapper import get_reviews, get_name
from yt_search import search_videos
from flask_sq

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('loggedin.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    pw = request.form.get('password')
    return '',200

@app.route('/submit_form', methods=['POST'])
def submit_form():
    
    url = request.form.get('url')
    id = request.form.get('id')

    return comment_analysis(url, id)

@app.route('/submit_amz_form', methods=['POST'])
def submit_amz_form():
    
    url = request.form.get('url')
    lang = request.form.get('lang')
    response = get_reviews(url, lang)
    positives, negatives = response
    videos = search_videos(get_name(url), 3, lang)
    return jsonify({'positives': positives, 'negatives': negatives, 'videos': videos})
    

if __name__ == '__main__':
    app.run(debug=True)