from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os
from dotenv import load_dotenv  

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")  
)

audio = client.generate(
    text="This resume sucks. Stop playing league of legends and get some projects",
    voice="s2wvuS7SwITYg8dqsJdn",
    model="eleven_multilingual_v2"
)

save(audio, "output.mp3")