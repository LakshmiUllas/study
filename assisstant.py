# study
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_API_KEY = "YOUR_API_KEY"
GOOGLE_CSE_ID = "YOUR_CSE_ID"

def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    response = requests.get(url)
    results = response.json().get('items', [])
    return [item['snippet'] for item in results[:3]]  # Take top 3 snippets

def verify_answer(snippets):
    # Basic majority agreement: if most snippets are similar, use them
    from difflib import SequenceMatcher
    threshold = 0.75
    for i, s1 in enumerate(snippets):
        agree = 1
        for j, s2 in enumerate(snippets):
            if i != j:
                if SequenceMatcher(None, s1, s2).ratio() > threshold:
                    agree += 1
        if agree >= 2:  # 2 out of 3 agree
            return s1
    return None

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json['query']
    snippets = google_search(user_query)
    answer = verify_answer(snippets)
    if answer:
        response = f"Hey! Here’s what I found: {answer}"
    else:
        response = "Sorry, I couldn’t find a reliable answer to that right now."
    return jsonify({'answer': response})

if __name__ == "__main__":
    app.run()
