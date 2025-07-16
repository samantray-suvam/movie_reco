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
    if not query:
        return jsonify({'error': 'No search query provided'}), 400

    try:
        headers = {
            'Authorization': f'Bearer {QLOO_API_KEY}',
            'Content-Type': 'application/json'
        }

        # Search for movies
        movie_response = requests.post(
            f'{QLOO_BASE_URL}/recommendations/get_similar_items',
            headers=headers,
            json={
                "item": {
                    "type": "MOVIE",
                    "title": query
                },
                "limit": 6
            }
        )

        # Search for books
        book_response = requests.post(
            f'{QLOO_BASE_URL}/recommendations/get_similar_items',
            headers=headers,
            json={
                "item": {
                    "type": "BOOK",
                    "title": query
                },
                "limit": 6
            }
        )

        results = {
            'movies': movie_response.json().get('recommendations', []),
            'books': book_response.json().get('recommendations', [])
        }
        
        return jsonify(results)
    except Exception as e:
        print(f"Search error: {str(e)}")  # For debugging
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
