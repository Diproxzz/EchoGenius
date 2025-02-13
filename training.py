import pyttsx3
import speech_recognition as sr
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 200)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=10, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        return "none"
    query = query.lower()
    return query

with open('intents.json', 'r') as file:
    intents = json.load(file)

# Load the model and tokenizer
loaded_model = tf.keras.models.load_model('intent_model.h5')
loaded_tokenizer = Tokenizer()
loaded_tokenizer.word_index = np.load('intent_tokenizer.npy', allow_pickle=True).item()

# Function to predict intent
def predict_intent(text):
    sequence = loaded_tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=6, padding='post')
    prediction = loaded_model.predict(padded_sequence)[0]
    intent_index = np.argmax(prediction)
    confidence = prediction[intent_index]
    intent_label = list(intents.keys())[intent_index]

    print(f"Predicted Intent: {intent_label}")

    responses = intents[intent_label].get("responses")
    response = random.choice(responses)
    return response, confidence, intent_label

speak("Speak the query: ")
query = takecommand()
response, confidence, intent_label = predict_intent(query)
if confidence > 0.5:
    if response in intents[intent_label]['responses']:
        response = random.choice(intents[intent_label]["responses"])
        speak(response)

else:
    speak("Bot: I'm sorry, I didn't understand that.")
