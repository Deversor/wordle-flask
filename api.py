from flask import Blueprint, jsonify, request
import json
import os

api = Blueprint('api', __name__)
WORDS_FILE = 'words.json'

def init_words_file():
    if not os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, 'w') as f:
            json.dump([], f)

def load_words():
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE) as f:
            return json.load(f)
    return []

def save_words(words):
    with open(WORDS_FILE, 'w') as f:
        json.dump(words, f)

@api.route('/api/words', methods=['GET'])
def get_words():
    return jsonify(load_words()), 200

@api.route('/api/words/<string:word>', methods=['GET'])
def get_word(word):
    words = load_words()
    if word in words:
        return jsonify({'word': word}), 200
    return jsonify({'error': 'Word not found'}), 404

@api.route('/api/words', methods=['POST'])
def add_word():
    data = request.get_json(silent=True) or {}
    word = data.get('word')
    if not word:
        return jsonify({'error': 'Word is required'}), 400
    words = load_words()
    if word in words:
        return jsonify({'error': 'Word already exists'}), 400
    words.append(word)
    save_words(words)
    return jsonify({'message': 'Word added'}), 201


@api.route('/api/words/<string:old_word>', methods=['PUT'])
def update_word(old_word):
    data = request.get_json(silent=True) or {}
    new_word = data.get('word')
    if not new_word:
        return jsonify({'error': 'New word is required'}), 400
    words = load_words()
    if old_word not in words:
        return jsonify({'error': 'Original word not found'}), 404
    idx = words.index(old_word)
    words[idx] = new_word
    save_words(words)
    return jsonify({'message': 'Word updated'}), 200

@api.route('/api/words/<string:word>', methods=['DELETE'])
def delete_word(word):
    words = load_words()
    if word not in words:
        return jsonify({'error': 'Word not found'}), 404
    words.remove(word)
    save_words(words)
    return jsonify({'message': 'Word deleted'}), 200



init_words_file()
