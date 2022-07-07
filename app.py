import pickle as pk

from flask import Flask, request, jsonify

import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences



app = Flask(__name__)

def encode_sequences(tokenizer, length, lines):
    # integer encode sequences
	X = tokenizer.texts_to_sequences(lines)
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=length, padding='post')
	return X

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None
 
# generate target given source sequence
def predict_sequence(model, tokenizer, source):
	prediction = model.predict(source, verbose=0)[0]
	integers = [np.argmax(vector) for vector in prediction]
	target = list()
	for i in integers:
		word = word_for_id(i, tokenizer)
		if word is None:
			break
		target.append(word)
	return ' '.join(target)

@app.route('/translate', methods=["POST"])
def translate():
    request_data = request.json
    input_text = np.array([request_data['input_text']])
    source_lang = request_data['source_lang']
    dest_lang = request_data['dest_lang']
    
    # Load model
    model = load_model('models/model_v1.h5')
    
    # load model parameters
    model_parameters = pk.load(open("models/model_parameter_v1.pk","rb"))
    
    if source_lang=="en" and dest_lang=="deu" :
        encode_input =encode_sequences(model_parameters['fren_tokenizer'], model_parameters["gho_length"], input_text)
        translated = predict_sequence(model,model_parameters["gho_tokenizer"], encode_input)
        return jsonify({"result":translated})
    elif source_lang=="deu" and dest_lang=="en": 
        encode_input = encode_sequences(model_parameters['gho_tokenizer'], model_parameters["gho_length"], input_text)
        translated = predict_sequence(model,model_parameters["fren_tokenizer"], encode_input)
        return jsonify({"result":translated})
    else:
        return jsonify({"result":"Error"})
    

if __name__=="__main__":
    app.run(port=8000, debug=True)