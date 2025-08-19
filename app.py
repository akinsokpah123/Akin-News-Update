# app.py
from flask import Flask, render_template_string
import requests
import os

# Set your API key here (or via environment variable)
API_KEY = os.getenv("NEWS_API_KEY", "5504467baaba92636240eb3b2dd1b063")
API_URL = "https://newsapi.org/v2/top-headlines?language=en&pageSize=20&apiKey=" + API_KEY

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Global News Updates</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }
    header { background: #333; color: white; padding: 20px; text-align: center; }
    .container { width: 80%; margin: 20px auto; }
    .news-item { background: white; padding: 15px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    .news-item h3 { margin: 0 0 10px 0; }
    .news-item p { margin: 0; }
    a { color: #1a73e8; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <header>
    <h1>🌎 Global News Updates</h1>
  </header>
  <div class="container">
    {% for article in articles %}
      <div class="news-item">
        <h3>{{ article['title'] }}</h3>
        <p>{{ article['description'] or 'No description available.' }}</p>
        {% if article['url'] %}
          <p><a href="{{ article['url'] }}" target="_blank">Read more</a></p>
        {% endif %}
        <p><small>Source: {{ article['source']['name'] }}</small></p>
      </div>
    {% endfor %}
  </div>
</body>
</html>
"""

@app.route("/")
def home():
    try:
        response = requests.get(API_URL)
        data = response.json()
        articles = data.get("articles", [])
    except Exception as e:
        articles = []
        print("API error:", e)
    return render_template_string(HTML_TEMPLATE, articles=articles)

@app.route("/healthz")
def health_check():
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
