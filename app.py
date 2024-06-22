import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

COSMOS_URL = 'https://esiexchange.documents.azure.com:443/'

credential = DefaultAzureCredential()
client = CosmosClient(url=COSMOS_URL, credential=credential)
database = client.get_database_client('exchange')
container = database.get_container_client('exchange')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/home')
def home():
    headers = request.headers
    principal = headers.get('X-MS-CLIENT-PRINCIPAL')
    user = container.read_item(
        'matthewmcintire@gmail.com',
        'user'
    )
    return str(principal)

if __name__ == '__main__':
    app.run()