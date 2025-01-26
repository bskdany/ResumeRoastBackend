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

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
task_queue = queue.Queue()

FILE_PATH = "generated.mp3"
lock = threading.Lock()
generation_done = threading.Event()

@app.route('/healthz')
def health_check():
    return 'OK', 200
 

@app.get('/add-audio')
def add_audio():
    task_queue.put(1)
    return jsonify({"status": "success", "message": "Task added to queue"}), 200

@app.get('/get-audio')
def generate_audio():
    if task_queue.empty():
        return jsonify({"status": "error", "message": "No tasks in queue"}), 200


    else:
        # I'M OUT OF CREDITS AAAAAA
        
        # audio = client.generate(
        #     text="This resume sucks. Stop playing league of legends and get some projects going",
        #     voice="s2wvuS7SwITYg8dqsJdn",
        #     model="eleven_multilingual_v2"
        # )
            
        # save(audio, "generated.mp3")

        task_queue.get()

        return send_from_directory(
            "./",
            'generated.mp3',  # Replace with your filename
            mimetype='audio/mpeg'
        )

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)