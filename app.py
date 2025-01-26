from flask import Flask, jsonify
from flask import Blueprint
from flask import Response, request
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv  
import time
import queue
import threading
from flask_cors import CORS  

bp = Blueprint('main', __name__)
load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")  
)

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

from flask import Flask, request
from flask import redirect, render_template, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, PartitionKey
import random
from dotenv import load_dotenv
import string, random, requests

load_dotenv() 
account = os.getenv('ACCOUNT')
key = os.getenv('KEY')
container = os.getenv('CONTAINER')
cosmos_endpoint = os.getenv('COSMOS_ENDPOINT')
cosmos_key = os.getenv('COSMOS_KEY')
cosmos_database_name = os.getenv('COSMOS_DATABASE_NAME')
cosmos_container_name = os.getenv('COSMOS_CONTAINER_NAME')
storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
task_queue = queue.Queue()

# Initialize the BlobServiceClient
client_blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
container_blob = client_blob_service_client.get_container_client(container)

# Initialize the CosmosClient
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
cosmos_database = cosmos_client.get_database_client(cosmos_database_name)
cosmos_container = cosmos_database.get_container_client(cosmos_container_name)

FILE_PATH = "generated.mp3"
lock = threading.Lock()
generation_done = threading.Event()

@app.route('/healthz')
def health_check():
    return 'OK', 200
 

@app.route('/form', methods=['POST'])
def form():
    file = request.files['cv']
    filename = secure_filename(file.filename)
    file_extension = filename.rsplit('.', 1)[1]
    random_filename = id_generator()
    filename = random_filename + '.' + file_extension
    try:
        blob_client_test = container_blob.get_blob_client(filename)
        blob_client_test.upload_blob(data=file, overwrite=True)
    except Exception as e:
        print(f'Exception={e}')
        pass
    ref = f'https://{account}.blob.core.windows.net/{container}/{filename}'

    name = request.form.get('name')
    job_title = request.form.get('jobTitle')
    tolerance = request.form.get('tolerance')
    entity = {
        'id': random_filename,
        'name': name,
        'jobTitle': job_title,
        'tolerance': tolerance,
        'blobStorageRef': ref,
        'feedbackText': '',
        'isRead': False
    }
    try:
        cosmos_container.create_item(body=entity)
    except Exception as e:
        print(f'Exception={e}')
        pass
    return 'Created',201

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)