# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, request, jsonify, render_template
import openai

# Initialize Flask app
app = Flask(__name__)

# Configuration for OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to perform web crawling
def fetch_competitor_prices(query):
    # Example function to fetch prices from a website (placeholder)
    url = f'https://example.com/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Parse the HTML to extract pricing details (placeholder)
    items = soup.find_all('div', class_='item')
    data = []
    for item in items:
        title = item.find('h2').text
        price = item.find('span', class_='price').text
        data.append({'title': title, 'price': price})
    
    return pd.DataFrame(data)

# Function to query using OpenAI's language model
def query_llm(query):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=query,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Route for the web query interface
@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query = request.form['query']
        llm_response = query_llm(query)
        competitor_prices = fetch_competitor_prices(query)
        return render_template('result.html', llm_response=llm_response, competitor_prices=competitor_prices.to_html())
    return render_template('query.html')

# Dashboard route to display comparison
@app.route('/dashboard')
def dashboard():
    # Example data (placeholder)
    data = {
        'item': ['Item1', 'Item2', 'Item3'],
        'competitor1_price': [10, 20, 30],
        'competitor2_price': [11, 19, 29],
    }
    df = pd.DataFrame(data)
    return render_template('dashboard.html', tables=[df.to_html()], titles=df.columns.values)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
