from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback

speech_to_text = SpeechToTextV1(
    username='45050c73-0742-456d-b4d3-0c7a7435e53c',
    password='YwAANLIzlL8B',
    url='https://stream.watsonplatform.net/speech-to-text/api')

print(json.dumps(speech_to_text.list_models(), indent=2))

print(json.dumps(speech_to_text.get_model('en-US_BroadbandModel'), indent=2))

with open(join(dirname(__file__), '/resources/speech.wav'),
          'rb') as audio_file:
    print(
        json.dumps(
            speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                timestamps=True,
                word_confidence=True),
            indent=2))

# Example using websockets


class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        with open("transcript.txt", "w") as text_file:
            text_file.write("Transcript: %s " % transcript)
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_transcription_complete(self):
        print('Ali STT transcription test completed')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)


mycallback = MyRecognizeCallback()
with open(join(dirname(__file__), '/resources/speech.wav'),
          'rb') as audio_file:
    speech_to_text.recognize_with_websocket(
        audio=audio_file, recognize_callback=mycallback)
