from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load translation pipelines
en_to_fr_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr", tokenizer="Helsinki-NLP/opus-mt-en-fr")
fr_to_en_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en", tokenizer="Helsinki-NLP/opus-mt-fr-en")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    language = data.get('language')

    if language == 'en-US':
        translated_text = en_to_fr_translator(text)[0]['translation_text']
    elif language == 'fr-FR':
        translated_text = fr_to_en_translator(text)[0]['translation_text']
    else:
        translated_text = "Error: Unsupported language"

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)
