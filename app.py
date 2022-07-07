from flask import Flask, request, jsonify,render_template

import numpy as np

from utils import *

app = Flask(__name__)


@app.route('/translate', methods=["POST","GET"])
def translate():
    if request.method == "POST":      
        if request.is_json:
            request_data = request.json
            input_text = np.array([request_data['input_text']])
            source_lang = request_data['source_lang']
            dest_lang = request_data['dest_lang']
            
            translated = make_translation(source_lang, dest_lang, input_text)
            return jsonify({"result":translated})
        else:
            input_text = np.array([request.form['input_text']])
            source_lang = request.form['source_lang']
            dest_lang = request.form['dest_lang']
            
            translated = make_translation(source_lang, dest_lang, input_text)

            return render_template('index.html', translated=translated, input_text=request.form['input_text'])
    elif request.method == "GET":
        return render_template('index.html')
    
    
@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')

if __name__=="__main__":
    app.run(port=8000, debug=True)