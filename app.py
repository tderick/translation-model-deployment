from flask import Flask, request

app = Flask(__name__)

@app.route('/translate', methods=["POST"])
def translate():
    request_data = request.json
    input_text = request_data['input']

if __name__=="__main__":
    app.run(port=8000, debug=True)