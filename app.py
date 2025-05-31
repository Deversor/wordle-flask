from flask import Flask, render_template, jsonify, request
from api import api
import nltk, random
from nltk.corpus import brown, words
import json

app = Flask(__name__)

app.register_blueprint(api)
try:
    brown_words = set(brown.words())

    nltk_words = set(words.words())

    combined_word_list = brown_words.union(nltk_words)
    word_list = [word.lower() for word in combined_word_list if len(word) == 5 and word.isalpha()]

except RuntimeError: # if the corpora (word lists) arent downloaded
    nltk.download('brown')
    nltk.download('words')

    brown_words = set(brown.words())

    nltk_words = set(words.words())

    combined_word_list = brown_words.union(nltk_words)
    word_list = [word.lower() for word in combined_word_list if len(word) == 5 and word.isalpha()]


@app.route('/') # base route
def index():
    return render_template('index.html')

@app.route('/words')
def words_page():
    return render_template('words.html')

@app.route('/word_api', methods=['GET'])
def word_api():
    word = random.choice(word_list)
    return jsonify({'word' : word.upper()})

@app.route('/check', methods=['POST'])
def check():
    word_object = request.get_json()
    word = word_object['word'].lower()

    # Load user-added words from words.json
    try:
        with open('words.json') as f:
            custom_words = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        custom_words = []

    # Combine built-in and custom word lists
    all_words = set(word_list).union(set(custom_words))

    is_in_word_list = word in all_words

    return jsonify({"is_in_word_list": is_in_word_list})



if __name__ == '__main__':
    app.run(debug=True)