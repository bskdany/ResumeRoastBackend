import os
import io
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
api_key = os.getenv('SPEECH_API_KEY')
endpoint = os.getenv('SPEECH_ENDPOINT')
region = os.getenv('SPEECH_REGION')

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_API_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_config.speech_synthesis_voice_name='it-IT-LisandroNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

text = """
Hello, this is a test of the speech synthesis service.""".strip()
speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()