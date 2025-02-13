import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json


# Example intents data
intents = {
    "start":{
        "patterns": ["hey echo","wakeup","wake up","hello","hi","hi echo","hello echo","buddy","hey buddy","wakeup buddy","wake up buddy","hello echogenius","wake up echogenius","wakeup echogenius","hi echogenius"],
        "responses": [" "]
    },
    "identity": {
        "patterns": ["who are you","who r u","who r you","who are u","what is your name","what's your name",
                     "introduce yourself","tell me your identity","what is your identity","what's your identity"],
        "responses": ["I'm EchoGenius, your new personal assistant","It is EchoGenius this side",
                      "My name is EchoGenius, how can I assist you?","Hi, I am EchoGenius. How can I help you?"]
    },
    "personal_info": {
        "patterns": ["when were you born","what is your birthdate","what's your birthdate","when is your birthday",
                    "who designed you","who made you","who programmed you"],
        "responses": ["I am a computer software made by Mr. Dipro Chowdhury in the year 2023.",
                      "I am designed by Mr. Dipro Chowdhury in 2023. I am still under development.",
                      "I don't have a specific birthdate as I am still under development. Mr. Dipro started my development."]
    },
    "greetings": {
        "patterns": ["hello", "hi", "hey", "howdy", "greetings", "good morning", "good afternoon", "good evening",
                     "hi there", "hey there", "what's up", "hello there"],
        "responses": ["Hello! How can I assist you?", "Hi there!", "Hey! What can I do for you?",
                      "Howdy! What brings you here?", "Greetings! How may I help you?",
                      "Greetings! How can I be of service?", "Greetings sir! What do you need assistance with?",
                      "Greetings! How may I assist you?", "Hey there! How can I help?", "Hi! What's on your mind?",
                      "Hello there! How can I assist you today?"]
    },
    "goodbye": {
        "patterns": ["bye", "quit the program", "quit", "exit", "see you later", "good bye", "tata", "see you soon",
                     "goodbye", "adieu", "goodbye candy", "farewell", "take care", "until next time", "bye bye",
                     "catch you later", "have a good one", "see you"],
        "responses": ["Goodbye!", "See you later!", "Have a great day!", "Farewell! Take care.",
                      "Goodbye! Until next time.", "Take care! Have a wonderful day.", "Bye bye!", "Catch you later!",
                      "Have a nice one!", "Thank you for using me sir, have a good day. "]
    },
    "gratitude": {
        "patterns": ["thank you", "thanks", "appreciate it", "thank you so much", "thanks a lot", "much appreciated"],
        "responses": ["You're welcome!", "Happy to help!", "Glad I could assist.", "Anytime!",
                      "You're welcome! Have a great day.", "No problem!"]
    },
    "wellbeing": {
        "patterns": ["how are you", "how r u", "how you doing", "whats up", "all good", "everything good", "all fine",
                     "all ok"],
        "responses": ["Sir, it's my pleasure to serve you.",
                      "Yes, I'm here and ready to help! If you have any questions or if there's anything specific you'd like assistance with, feel free to let me know.",
                      "Thank you for asking! As a computer program, I don't have feelings, but I'm here and ready to assist you. How can I help you today?",
                      "Hello! I'm here and ready to help. If you have any questions or if there's something specific you'd like to know or discuss, feel free to let me know!"]
    },
    "image_recognition":{
        "patterns": ["identify image","recognize image","image identification","image recognition"],
        "responses": ["Enter the path or name of the image: ","Mention the image's path: ","Where is the image located? "]
    },
    "notepad": {
        "patterns": ["open notepad", "can you open notepad", "edit notepad", "activate notepad", "start notepad"],
        "responses": ["Opening Notepad.", "Starting Notepad.", "Enabling Notepad editing."]
    },
    "close_notepad": {
        "patterns": ["close notepad", "exit notepad", "stop notepad", "quit notepad", "terminate notepad"],
        "responses": ["Closing Notepad.", "Quitting Notepad.", "Exiting Notepad."]
    },
    "cmd": {
        "patterns": ["open command prompt", "start command prompt"],
        "responses": ["Opening command prompt.", "Starting command prompt."]
    },
    "close_command_prompt": {
        "patterns": ["close command prompt", "exit command prompt","quit command prompt"],
        "responses": ["Closing command prompt.", "Quitting command prompt.","Exiting command prompt."]
    },
    "apologies": {
        "patterns": ["sorry", "my apologies", "apologize", "I'm sorry"],
        "responses": ["No problem at all.", "It's alright.", "No need to apologize.", "That's okay.",
                      "Don't worry about it.", "Apology accepted."]
    },
    "positive_feedback": {
        "patterns": ["great job", "well done", "awesome", "fantastic", "amazing work", "excellent"],
        "responses": ["Thank you! I appreciate your feedback.", "Glad to hear that!", "Thank you for the compliment!",
                      "I'm glad I could meet your expectations.", "Your words motivate me!",
                      "Thank you for your kind words."]
    },
    "negative_feedback": {
        "patterns": ["not good","you are shit", "disappointed", "unsatisfied", "poor service", "needs improvement",
                     "you are disappointing","could be better"],
        "responses": ["I'm sorry to hear that. Can you please provide more details so I can assist you better?",
                      "I apologize for the inconvenience. Let me help resolve the issue.",
                      "I'm still under development. Sorry for the inconvenience."
                      "I'm sorry you're not satisfied. Please let me know how I can improve.",
                      "Your feedback is valuable. I'll work on improving."]
    },
    "camera": {
        "patterns": ["open camera", "switch on camera", "turn on camera", "activate the camera"],
        "responses": ["Starting camera.", "Opening camera.", "Turning on camera."]
    },
    "ip_address": {
        "patterns": ["what is my ip address", "what's my ip address", "tell my ip address", "ip address",
                     "tell ip address"],
        "responses": ["Your IP Address is: "]
    },
    "scan_qr": {
        "patterns": ["scan qr","scan a qr","scan qr code","scan a qr code","open a qr","decode a qr code","decode a qr"],
        "responses": ["Opening QR code scanner.","Opening QR code decoder."]
    },
    "qrcode_generator": {
        "patterns": ["generate a qr code","qr code generator","generate qr"
                     "make a qr code","generate a qr code for me","make a qr code for me"],
        "responses": [" "]
    },
    "youtube": {
        "patterns": ["open youtube", "start youtube"],
        "responses": ["Starting youtube.", "Opening youtube."]
    },
    "facebook": {
        "patterns": ["open facebook", "open my facebook account", "start facebook"],
        "responses": ["Starting facebook.", "Opening facebook.", "Opening your facebook account."]
    },
    "twitter": {
        "patterns": ["open twitter", "open my twitter account", "start twitter","open x", "open my x account", "start x"],
        "responses": ["Starting twitter.", "Opening twitter.", "Opening your twitter account.","Starting x.", "Opening x.", "Opening your x account."]
    },
    "help": {
        "patterns": ["help", "can you help me?", "I need assistance", "support"],
        "responses": ["Sure, I'll do my best to assist you.", "Of course, I'm here to help!", "How can I assist you?", "I'll help you with your query."]
    },
    "instagram": {
        "patterns": ["open instagram", "open insta", "start insta", "open my insta account",
                     "open my instagram account", "start instagram"],
        "responses": ["Starting instagram.", "Opening instagram.", "Opening your instagram account."]
    },
    "google": {
        "patterns": ["open google", "start google"],
        "responses": ["Starting google.", "Opening google."]
    },
    "whatsapp": {
        "patterns": ["send a message", "whatsapp", "send a message through whatsapp", "open whatsapp",
                     "send a message via whatsapp"],
        "responses": ["Opening whatsapp."]
    },
    "mobile_camera": {
        "patterns": ["open mobile camera", "start mobile camera", "use mobile camera", "enable mobile camera"],
        "responses": ["Starting mobile camera.", "Enabling mobile camera.", "Opening mobile camera"]
    },
    "twitterbot": {
        "patterns": ["post on twitter", "post on x","post message on twitter","post message on x"],
        "responses": ["What do you want to post?","What do you wish to post?","What would you like to post on twitter?","What would you like to post on x?"]     
    },
    "song_yt": {
        "patterns": ["play a song on youtube", "song on youtube", "play music on youtube","play songs on youtube",
                     "play music", "music on youtube"],
        "responses": ["Tell the name of the song.", "Which song you want to play?", "What song would you like?"]
    },
    "gmail": {
        "patterns": ["email", "gmail", "send a mail", "can you send a mail"],
        "responses": ["Activating Gmail."]
    },
    "alarm": {
        "patterns": ["can you set an alarm", "set alarm", "set an alarm"],
        "responses": ["Please tell the time to set the alarm. For example: Set alarm to 6:30 am."]
    },
    "jokes": {
        "patterns": ["tell me a joke", "joke please", "got any jokes?", "make me laugh"],
        "responses": ["Here is one: "]
    },
    "switch_window": {
        "patterns": ["switch window", "switch the window", "change window", "change the window"],
        "responses": ["Switching window."]
    },
    "news": {
        "patterns": ["tell me news", "news please", "fetch me news", "fetch me the latest news", "any news update",
                     "news update"],
        "responses": ["Fetching news. Please wait.", "Fetching the latest news.",
                      "Please wait while I fetch the latest news."]
    },
    "location": {
        "patterns": ["where am i", "where are we", "what's my location", "what is my location", "location please",
                     "trace me", "locate me"],
        "responses": ["We are in ", "You are in ", "Our location is ", "Your location is "]
    },
    "profile_instagram": {
        "patterns": ["view profile on instagram", "profile on instagram", "instagram profile",
                     "find instagram profile"],
        "responses": ["Which profile you want to find? ", "Enter the profile id: ",
                      "What is the profile id of the account? "]
    },
    "screenshot": {
        "patterns": ["take a screenshot", "screenshot", "capture what is in the window",
                     "capture what's in the window"],
        "responses": [" "]
    },
    "read_pdf": {
        "patterns": ["read a pdf", "can you read a pdf", "read the pdf", "please read the pdf"],
        "responses": ["Enter the path of the pdf: ", "Which pdf you want to read? "]
    },
    "calculation": {
        "patterns": ["can you calculate", "please calculate", "calculate", "do the calculation"],
        "responses": ["What do you want to calculate? "]
    },
    "temperature": {
        "patterns": ["what is the temperature", "temperature", "what's the temperature", "tell the temperature",
                     "tell me the temperature"],
        "responses": [" "]
    },
    "how_to_do": {
        "patterns": ["activate how to do", "activate how to do mode"],
        "responses": ["How to do mode activated.", "Enabling how to do mode", "How to do mode enabled"]
    },
    "battery": {
        "patterns": ["how much battery left", "what is the battery percent", "what's the battery percent",
                     "what is the battery percentage", "what's the battery percentage", "how much battery left",
                     "remaining battery"],
        "responses": [" "]
    },
    "internet_speed": {
        "patterns": ["check internet speed", "check the internet speed", "check our internet speed",
                     "tell our internet speed", "tell me the internet speed", "tell the internet speed",
                     "what is the internet speed", "what's the internet speed", "what's our internet speed",
                     "what's our internet speed"],
        "responses": ["Checking internet speed", "Calculating internet speed"]
    },
    "volume_increase": {
        "patterns": ["increase volume", "increase the volume"],
        "responses": [" "]
    },
    "volume_decrease": {
        "patterns": ["decrease volume", "decrease the volume"],
        "responses": [" "]
    },
    "volume_mute": {
        "patterns": ["mute", "mute the system", "turn off the volume"],
        "responses": [" "]
    },
    "shut_down": {
        "patterns": ["shutdown", "shutdown the system", "switch off", "power off", "close the system"],
        "responses": ["Shutting down", "Closing the system", "Switching off"]
    },
    "restart": {
        "patterns": ["restart", "restart the system", "start the system again"],
        "responses": ["Restarting the system"]
    },
    "sleep": {
        "patterns": ["put the machine to sleep", "sleep the system", "put the system to sleep",
                     "put the device to sleep", "sleep the machine"],
        "responses": ["Putting the system to sleep"]
    },
    "hibernate": {
        "patterns": ["hibernate the system", "hibernate"],
        "responses": ["Hibernating the system"]
    },
    "search": {
        "patterns": ["chat", "chatbot", "answer me", "search"],
        "responses": [" "]
    },
    "close": {
        "patterns": ["close", "exit", "quit", "leave the page"],
        "responses": [" "]
    },
    "search_file": {
        "patterns": ["search a file","open file","display a file"],
        "responses": ["Enter the name of the file: ","Which file you want to open? ","What is the name of the file?"]
    },
    "silence": {
        "patterns": ["take rest","sleep for now","sleep now","sleep","take a nap"],
        "responses": ["Going to sleep.","As you wish. Call me whenever you need me","Going to rest for a while. Call me whenever needed."]
    }
}

# Combine all patterns and responses for tokenization
all_patterns = [pattern for intent in intents.values() for pattern in intent["patterns"]]
all_responses = [response for intent in intents.values() for response in intent["responses"]]

# Tokenize the text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_patterns + all_responses)

# Convert text to sequences
sequences = tokenizer.texts_to_sequences(all_patterns)

# Pad sequences to have consistent length
max_sequence_length = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length, padding='post')
#print(max_sequence_length)

# Create input and output data
X = padded_sequences
y = np.array([i for i in range(len(intents)) for _ in intents[list(intents.keys())[i]]["patterns"]])

# Define the LSTM model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=50, input_length=max_sequence_length))
model.add(LSTM(100))
model.add(Dense(len(intents), activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=30, batch_size=1, verbose=2)


model.save("intent_model.h5")
np.save('intent_tokenizer.npy', tokenizer.word_index)

with open('intents.json', 'w') as file:
    json.dump(intents, file)