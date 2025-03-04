import json
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template

from gpt import extract_text_from_webpage, get_gpt_response

app = Flask(__name__)
CORS(app) 

@app.route('/check-compliance', methods=['POST'])
def check_compliance():
    try:
        data = request.json
    
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400
        
        url = data['url']
        webtext = extract_text_from_webpage(url)

        with open("./prompts/compliance_terms.txt", "r", encoding="utf-8") as file:
            compliance_terms = file.read()

        result = get_gpt_response(webtext, compliance_terms)
        result = json.loads(result)

        return result, 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()