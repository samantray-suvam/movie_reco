from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)
CORS(app)
load_dotenv()

QLOO_API_KEY = os.getenv('QLOO_API_KEY')
QLOO_BASE_URL = 'https://hackathon.api.qloo.com'  

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    try:
        # Replace this with actual QLOO API implementation
        headers = {
            'Authorization': f'Bearer {QLOO_API_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.get(
            f'{QLOO_BASE_URL}/search',
            headers=headers,
            params={'query': query}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
