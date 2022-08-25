from PyPDF2 import PdfReader
import requests
from google.cloud import texttospeech
import os

reader = PdfReader("example.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

# Google Credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "strong-bus-360519-3ee63dc64b56.json"


# Creates an instances of the Google Text to Speech Client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesised
synthesis_input = texttospeech.SynthesisInput(text=text)

# Build the voice request, select the language code ("en-US") and the Speech Synthesis Markup Language (ssml) voice
# gender ("neutral")
voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                          ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

# Output audio: mp3
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

try:
    # Synthesise the speech
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
except:
    print("PDF incompatible. Maybe 5000 characters limit exceeded?")
else:
    # Generate the mp3, wb means "write and binary" This is because the response's audio_content is binary
    with open("output.mp3", "wb") as file:
        file.write(response.audio_content)
        print("mp3 generated")


