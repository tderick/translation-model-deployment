from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/translate', methods=["POST"])
def translate():
    request_data = request.json
    input_text = request_data['input_text']
    source_lang = request_data['source_lang']
    dest_lang = request_data['dest_lang']
    
    return jsonify({"input_data":input_data,"source_lang":source_lang,"dest_lang":dest_lang})
    

if __name__=="__main__":
    app.run(port=8000, debug=True)