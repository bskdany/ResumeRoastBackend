from flask import Flask, request, jsonify
from flask import redirect, render_template, send_from_directory, url_for
import os
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, PartitionKey
import random
from dotenv import load_dotenv
import string, random
import queue
from flask_cors import CORS  
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import PyPDF2
from openai import OpenAI
import json

load_dotenv() 
account = os.getenv('ACCOUNT')
if(account == None):
    account = os.environ['ACCOUNT']
key = os.getenv('KEY')
if(account == None):
    account = os.environ['ACCOUNT']
container = os.getenv('CONTAINER')
if(account == None):
    account = os.environ['ACCOUNT']
cosmos_endpoint = os.getenv('COSMOS_ENDPOINT')
if(cosmos_endpoint == None):
    cosmos_endpoint = os.environ['COSMOS_ENDPOINT']
cosmos_key = os.getenv('COSMOS_KEY')
if(cosmos_key == None):
    cosmos_key = os.environ['COSMOS_KEY']
cosmos_database_name = os.getenv('COSMOS_DATABASE_NAME')
if(cosmos_database_name == None):
    cosmos_database_name = os.environ['COSMOS_DATABASE_NAME']
cosmos_container_name = os.getenv('COSMOS_CONTAINER_NAME')
if(cosmos_container_name == None):
    cosmos_container_name = os.environ['COSMOS_CONTAINER_NAME']
storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING') 
if(storage_connection_string == None):
    storage_connection_string = os.environ['AZURE_STORAGE_CONNECTION_STRING']

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Initialize the BlobServiceClient
client_blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
container_blob = client_blob_service_client.get_container_client(container)

# Initialize the CosmosClient
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
cosmos_database = cosmos_client.get_database_client(cosmos_database_name)
cosmos_container = cosmos_database.get_container_client(cosmos_container_name)

task_queue = queue.Queue()

FILE_PATH = "generated.mp3"

client_eleven_labs = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")  
)

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
        task_queue.put(random_filename)
    except Exception as e:
        print(f'Exception={e}')
        pass
    return 'Created',201

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.get('/add-audio')
def add_audio():
    task_queue.put(1)
    return jsonify({"status": "success", "message": "Task added to queue"}), 200

@app.get('/get-audio')
def generate_audio():
    if task_queue.empty():
        return jsonify({"status": "error", "message": "No tasks in queue"}), 200


    else:
        
        # audio = client.generate(
        #     text="This resume sucks. Stop playing league of legends and get some projects going",
        #     voice="s2wvuS7SwITYg8dqsJdn",
        #     model="eleven_multilingual_v2"
        # )
            
        # save(audio, FILE_PATH)

        task_queue.get()

        return send_from_directory(
            "./",
            FILE_PATH,  # Replace with your filename
            mimetype='audio/mpeg'
        )


def pdf_to_text(resume_path):

    # we should add a limit of how many chars we actually read
    with open(resume_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text        

def generate_roast(resume_content, job_title, tollerance):
    openai_key = os.getenv('OPENAI_KEY')
    print(openai_key)
    openai_client = OpenAI(api_key=openai_key, base_url="https://api.deepseek.com")

    completion = openai_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"You're a professional in the {job_title} field. You're given a resume by a candidate that you need to review depending on a roasting level, a level of 0 means constructive criticism, 100 means roast and borderline insult the person, your level is {tollerance}"},
            {"role": "user", "content": f"Here is the content from a PDF:\n\n{resume_content}"}
            ],
        max_tokens=100
    )

    return completion.choices[0].message

def get_blob_by_id(container_id):
    query = f"SELECT * FROM c WHERE c.id = @id"
    results = cosmos_container.query_items(
        query=query,
        parameters=[
            dict(
                name="@id",
                value = container_id
            )
        ],
        enable_cross_partition_query=False
    )

    for item in results:
        print(item)
        return item


    #     cosmos_container.read_item(item=container_id, partition_key=container_id)

        # for item in cosmos_container.query_items(
        #     query=query,
        #     enable_cross_partition_query=True
        #     ):
        #     print(json.dumbs(item))


        # items = list(cosmos_container.query_items(
        #     query=query,
        #     enable_cross_partition_query=True
        # ))

        # ref = f'https://{account}.blob.core.windows.net/{container}/{filename}'

        
        # if items:
            # print(items)
            # blob_ref = items[0]['blobStorageRef']
            # print(blob_ref)
            # return blob_ref
        # else:
        #     return None
    # except Exception as e:
    #     print(f'Exception={e}')
    #     return None



get_blob_by_id("0I2EE21CBA4T3AE09YYBAJ7FQEZ9S3V9")

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)