import os
import requests
import base64
from pypdf import PdfReader


# todo Implement file dialogue
# todo Implement reading pdf from weblink
def read_pdf():
    reader = PdfReader("TTS_test.pdf")
    page = reader.pages[0]
    text = page.extract_text(extraction_mode="layout")
    print("Text extracted")

    return text


def text_to_speech(text):
    # Configure request params
    tts_api_base_url = "https://api.sws.speechify.com/"
    tts_api_key = os.environ.get("tts_api_key")
    voice_id = "george"

    url = f"{tts_api_base_url}/v1/audio/speech"
    params = {
        "input": f"<speak>{text}</speak>",
        "voice_id": voice_id,
        "audio_format": "wav"
    }
    headers = {
        "Authorization": f"Bearer {tts_api_key}"
    }

    print("Converting to speech")

    # Send request to API
    response = requests.post(url=url, json=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Convert data to binary
    base64_audio_data = data["audio_data"]
    binary_audio_data = base64.b64decode(base64_audio_data)

    # Write data to audio file
    with open("output.wav", "wb") as audio_file:
        audio_file.write(binary_audio_data)

    print("Audio content saved as 'output.wav'")


# todo Create a separate module for tts synthesis which allows the user to select from different APIs and
#  modify options for the given API

if __name__ == '__main__':
    t = read_pdf()
    text_to_speech(t)
