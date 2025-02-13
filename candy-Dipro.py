import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import urllib.request
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
#from pyzbar.pyzbar import decode
import sys
import time
import pyjokes
import pyautogui
import requests
import numpy as np
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import PyPDF2
import operator
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import psutil
import speedtest_cli as spt
import MyAlarm
#from bardapi import BardCookies
from pysentimiento import create_analyzer
import pyperclip
from time import sleep
import json
import keyboard
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import qrcode
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
#from pysentimiento import create_analyzer
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

warnings.simplefilter('ignore')


# Develop engine for speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 200)


# Speak function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# Recognize speech command
def takecommand():
    try:        
        r = sr.Recognizer()
        
        with sr.Microphone() as source:            
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=10, phrase_time_limit=5)

        
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

    except Exception as e:
        # speak("Repeat that again please...")
        return "none"
    query = query.lower()
    return query


# Wish on starting the program
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if hour >= 0 and hour < 12:
        speak(f" Good morning, its {tt}")
    elif hour >= 12 and hour < 18:
        speak(f" Good afternoon, its {tt}")
    else:
        speak(f" Good evening, its {tt}")
    speak(" I am online sir. Tell me how can I help you? ")


with open('intents.json', 'r') as file:
    intents = json.load(file)

# Load the model and tokenizer
loaded_model = load_model('intent_model.h5')
loaded_tokenizer = Tokenizer()
loaded_tokenizer.word_index = np.load('intent_tokenizer.npy', allow_pickle=True).item()




#Removing a phrase which is not to be used in the function
def remove_starting_phrase(input_string):
    # Define patterns to match the starting phrases
    patterns = [
        r"^can you tell me\b",
        r"^can you assist me with\b",
        r"^can you help me with\b"
    ]

    # Join patterns with "|" to create a single regex pattern
    combined_pattern = "|".join(patterns)

    # Compile the regex pattern
    regex = re.compile(combined_pattern, flags=re.IGNORECASE)

    # Use sub() method to remove the matched pattern
    result = regex.sub("", input_string)

    return result.strip()




# Function to predict intent
def predict_intent(text):
    sequence = loaded_tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=6, padding='post')
    prediction = loaded_model.predict(padded_sequence)
    intent_index = np.argmax(prediction)
    intent_label = list(intents.keys())[intent_index]

    #print(f"Predicted Intent: {intent_label}")

    responses = intents[intent_label].get("responses")
    response = random.choice(responses)
    return response, intent_label


# Function to check if a pattern is present in any class
def check_pattern_class(pattern):
    for intent_label, intent_data in intents.items():
        if pattern in intent_data["patterns"]:
            return intent_label
    return "none"

# Tell news
def news():
    main_url = 'https://newsapi.org/v2/everything?q=keyword&apiKey=3eb8c67fddbb4dd9ac26aa65711ad800'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f" Today's {day[i]} news is: {head[i]}")


# Message via WhatsApp
def whatsapp_msg(to):
    data = {
        'me': "+919836924296",
        'ma': "+919051029231",
        'baba': "+919830124548",
        'shamim': "+918981404378",
        'shashank': "+916289321062",
        'dad': "+919007287548"
    }
    f = 0
    for key in data.keys():
        if to == key:
            f = 1
            return data.get(to)
    if f == 0:
        speak(" No such contacts found")
        return "none"




# Read PDF file
def pdf_reader(name):
    book = open(name, 'rb')
    pdfReader = PyPDF2.PdfReader(book)
    pages = len(pdfReader.pages)
    speak(f"There are {pages} pages in this book. Please enter the page number you want me to read: ")
    pg = int(input("Enter the page number:"))
    page = pdfReader.pages[pg-1]
    text = page.extract_text()
    speak(text)

'''
# Automate Copy Cookies of Bard
def CookieScrapper():
    webbrowser.open("https://bard.google.com")
    sleep(2)
    pyautogui.click(x=1682, y=74)
    sleep(1)
    pyautogui.click(x=1490, y=265)
    sleep(1)
    pyautogui.click(x=1405, y=120)
    sleep(1)
    keyboard.press_and_release('ctrl + w')

    data = pyperclip.paste()

    try:
        json_data = json.loads(data)
        pass

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")

    SID = "__Secure-1PSID"
    TS = "__Secure-1PSIDTS"
    CC = "__Secure-1PSIDCC"

    try:
        SIDValue = next((item for item in json_data if item["name"] == SID), None)
        TSValue = next((item for item in json_data if item["name"] == TS), None)
        CCValue = next((item for item in json_data if item["name"] == CC), None)

        if SIDValue is not None:
            SIDValue = SIDValue["value"]
        else:
            print(f"{SIDValue} not found in the JSON data.")

        if TSValue is not None:
            TSValue = TSValue["value"]
        else:
            print(f"{TSValue} not found in the JSON data.")

        if CCValue is not None:
            CCValue = CCValue["value"]
        else:
            print(f"{CCValue} not found in the JSON data.")

        cookie_dict = {
            "__Secure-1PSID": SIDValue,
            "__Secure-1PSIDTS": TSValue,
            "__Secure-1PSIDCC": CCValue,
        }

        return cookie_dict

    except Exception as e:
        print(e)


# Split the result of search in paragraphs
def split_and_save_paragraphs(data, filename):
    try:
        paragraphs = data.split('\n\n')
        with open(filename, 'w') as file:
            file.write(data)
        data = paragraphs[:]
        separator = ', '
        joined_string = separator.join(data)
        return joined_string
    except Exception as e:
        print(e)


# Search using Google-Bard
def MainExecution():
    cookie_dict = CookieScrapper()

    try:
        bard = BardCookies(cookie_dict=cookie_dict)
        print("The verification of cookies has been successfully completed.")
        print("")

    except Exception as e:
        print("*The verification of cookies has encountered an issue and has not been successful.*")
        print("*This issue may arise due to the unsuccessful extraction of cookies from the extension.*")
        print(e)
    while True:
        try:
            speak(" What do you want to search?")
            Question = takecommand()
            if Question in intents["close"].get("patterns"):
                break
            elif Question == "none":
                sleep(1)
            elif Question in intents["image_recognition"].get("patterns"):
                imagename = str(input("Enter The Image Name : "))
                image = open(imagename, 'rb').read()
                bard = BardCookies(cookie_dict=cookie_dict)
                results = bard.ask_about_image('what is in the image?', image=image)['content']
                current_datetime = datetime.datetime.now()
                formatted_time = current_datetime.strftime("%H%M%S")
                filenamedate = str(formatted_time) + str(".txt")
                filenamedate = "C:\\Users\\dipro\\OneDrive\\Desktop\\Code Editor\\Upgradation\\Database\\" + filenamedate
                res = (split_and_save_paragraphs(results, filename=filenamedate))
                speak(res)
            else:
                RealQuestion = str(Question)
                results = bard.get_answer(RealQuestion)['content']
                current_datetime = datetime.datetime.now()
                formatted_time = current_datetime.strftime("%H%M%S")
                filenamedate = str(formatted_time) + str(".txt")
                filenamedate = "C:\\Users\\dipro\\OneDrive\\Desktop\\Code Editor\\Upgradation\\Database\\" + filenamedate
                res = split_and_save_paragraphs(results, filename=filenamedate)
                speak(res)

        except Exception as e:
            print(e)


def scan_qr_code(file_path):
    image = cv2.imread(file_path)
    decoded_objects = decode(image)
    if decoded_objects:
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            webbrowser.open(data)
    else:
        print("No QR codes found in the image.")
'''

#Scan a qr code using camera
def scan_qr_code_camera():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        
        _, img = cap.read()
        data,one, _=detector.detectAndDecode(img)
        if data:
            a=data
            break
        cv2.imshow('QR Scanner',img)
        
        #if cv2.waitKey(1) == ord('x'):
        #    break
    b=webbrowser.open(str(a))
    cap.release(a)
    cap.destroyAllWindows()

#Fetch twitter account info
def account_info():
    with open('account_info.txt','r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]
        verify = info[2]
    return email,password, verify

#Identify which task is to be performed
def identify_intent(intent):
    if intent in intents:
        responses = intents[intent]['responses']
        response = random.choice(responses)
        # return response
        speak(response)

def search_and_open_file(filename, search_path="."):
    """Search for a file recursively in the specified search path and open it."""
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                try:
                    print(file_path)
                    return os.startfile(filepath = file_path)
                except:
                    print(f"File '{filename}' not found.")
                    pass  # Skip if there's an error opening the file
    return None


#Search using LLAMA model
def get_response(input_text):
    llm = CTransformers(model = 'C:/Users/dipro/OneDrive/Documents/models/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={'max_new_tokens':256,
                                'temperature':0.9})

    output = llm(input_text)
    return output

#Check if there is a word limit in the sentence
def check_string(input_text):
    pattern = r"in (\d+) words"
    match = re.search(pattern, input_text)
    if match:
        number = int(match.group(1))  # Extract the numeric part and convert to integer
        return number



# Function containing all the commands
def TaskExecution(counter):
    pyautogui.press('esc')
    speak("Welcome back sir")
    wish()
    while counter == True:
        query = takecommand()
        query1 = remove_starting_phrase(query)
        response, intent_class = predict_intent(query1)


        
    #    intent_class = check_pattern_class(query)

        if query == "none":
            continue

        if response != None and intent_class:
            speak(response)

        elif intent_class == "silence":
            counter=False



        if intent_class=="goodbye":
            counter = False
            sys.exit()


        elif intent_class == "notepad":
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)



        elif intent_class == "cmd":
            os.system("start cmd")

        elif intent_class == "close_command_prompt":
            os.system("taskkill /F /FI \"IMAGENAME eq cmd.exe\" /T")


        elif intent_class == "camera":
            try:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    if cv2.waitKey(10) == ord("x"):
                        break
                cap.release()
                cv2.destroyAllWindows()
            except Exception:
                speak("Sorry sir, I am unable to perform the task.")



        elif intent_class == "mobile_camera":
            try:
                URL = "http://192.168.0.107:8080"
                while True:
                    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
                    img = cv2.imdecode(img_arr, -1)
                    cv2.imshow('IPWebcam', img)
                    q = cv2.waitKey(1)
                    if q == ord("x"):
                        break
                cv2.destroyAllWindows()
            except Exception:
                speak("Sorry sir, I am unable to perform the task.")



        elif intent_class == "ip_address" :
            try:
                ip = get('https://api.ipify.org').text
                speak(f" Your IP address is {ip}")
            except Exception:
                speak("Sorry sir, I could not fetch your IP address.")


        elif intent_class == "search_file" :
#            try:
            filename = input(str("File name: "))
            search_and_open_file(filename)
#            except:
#                print("Sorry sir, I could not find the file you want to search")

        elif "wikipedia" in query:
            speak(" Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak(" According to Wikipedia ")
            speak(results)

        elif intent_class == "qrcode_generator":
            try:
                c=0
                qr = qrcode.QRCode(version=1,
                                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                                   box_size=50,
                                   border=1)
                url = input("Enter the URL or the text: ")
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                while c==0:
                    speak("Tell the name of the QR code generated: ")
                    name = takecommand()
                    c=1
                    if name=="none":
                        c=0
                file_path = f"C:/Users/dipro/OneDrive/Desktop/Code Editor/Upgradation/QR-Codes/{name}.png"
                img.save(file_path)
            except Exception:
                speak("Sorry sir, I am unable to generate the QR code.")

        elif intent_class == "scan_qr":
            try:
                c = 0
                while c==0:
                    speak("Scan a QR code by path or by camera. "
                          "Say 'file location' for scanning by path "
                          "or 'camera' for scanning by using the camera.")
                    cm = takecommand()
                    c = 1
#                    if cm == "file location":
#                        file_path = input("Enter the path of the image file: ")
#                        scan_qr_code(file_path)
                    if cm == "camera":
                       scan_qr_code_camera()
                    elif cm =="none":
                        c=0
                    else:
                        speak("Nothing to scan")
            except:
                #continue
                speak("Unable to scan")


        elif intent_class == "youtube":
            webbrowser.open("www.youtube.com")

        elif intent_class == "instagram":
            webbrowser.open("www.instagram.com")


        elif intent_class == "facebook":
            webbrowser.open("www.facebook.com")

        elif intent_class == "twitter":
            webbrowser.open("www.twitter.com")

        elif intent_class == "google":
            try:
                speak(" What should I search in google?")
                cm = takecommand()
                webbrowser.open(f"{cm}")
            except Exception:
                speak("Sorry sir, I could not perform the task.")


        elif intent_class == "whatsapp":
            try:
                c = 0
                while c == 0:
                    speak("To whom should I send the message")
                    to = takecommand()
                    rec = whatsapp_msg(to)
                    c = 1
                    if rec == "none":
                        c = 0
                co = 0
                while co == 0:
                    speak("What should I send sir?")
                    msg = takecommand()
                    co += 1
                    if msg == 'none':
                        co = 0

                kit.sendwhatmsg_instantly(f"{rec}", f"{msg}")


            except Exception:
                speak("Sorry sir, I could not send the message.")


        elif intent_class == "song_yt":
            try:
                #speak("What song should I play?")
                query = takecommand()
                kit.playonyt(f"{query}")
            except Exception:
                speak("Sorry sir, I am unable to play the song.")


        elif intent_class == "gmail":
            try:
                co = 0
                smtp_port = 587
                smtp_server = "smtp.gmail.com"
                pswd = "mucn kksb dzht jukc"
                email_list = []
                speak("From which id I should send the mail?")
                email_from = input("Mail Id: ")
                speak("Whom to send the mail sir?")
                while True:
                    email_list.append(input("Receiver mail id: "))
                    speak(" Is that all sir?")
                    choice = takecommand()
                    if choice != 'no':
                        break
                while co == 0:
                    speak("What is the subject of the mail?")
                    subject = takecommand()
                    co += 1
                    if subject == "none":
                        co = co - 1

                def send_emails(email_list):
                    for person in email_list:
                        speak(" What should I say in the mail sir?")
                        body = takecommand()
                        msg = MIMEMultipart()
                        msg['from'] = email_from
                        msg['to'] = person
                        msg['subject'] = subject
                        count = 0
                        msg.attach(MIMEText(body, 'plain'))
                        while count == 0:
                            speak("Should I attach something in the mail sir?")
                            choice = takecommand()
                            count += 1
                            if choice == "none":
                                count = count - 1

                        if choice == "no thanks":
                            speak("No files attached")

                        else:
                            speak(" Please enter the file path:")
                            filename = input("File path: ")
                            attachment = open(filename, 'rb')
                            attachment_package = MIMEBase('application', 'octet-stream')
                            attachment_package.set_payload((attachment).read())
                            encoders.encode_base64(attachment_package)
                            attachment_package.add_header('Content-Disposition', "attachment; filename=" + filename)
                            msg.attach(attachment_package)

                        body = msg.as_string()
                        speak("Please wait while I connect to the server")
                        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
                        TIE_server.starttls()
                        TIE_server.login(email_from, pswd)
                        speak("Connected to the server")
                        print()
                        speak(f"Sending email to: {person}")
                        TIE_server.sendmail(email_from, person, body)
                        speak(f"Email sent successfully to : {person}")

                    TIE_server.quit()

                send_emails(email_list)
            except Exception:
                speak("Sorry sir, I am unable to send the mail.")




        elif intent_class == "close_notepad":
            x = "taskkill /f /im notepad.exe"
            os.system(x)

        elif intent_class == "alarm":
            try:
                speak("Please tell the time to set the alarm. For example: Set alarm to 6:30 am")
                tt = takecommand()
                tt = tt.replace("set alarm to ", "")
                tt = tt.replace(".", "")
                tt = tt.upper()
                speak(f"Alarm is set for {tt}")
                MyAlarm.alarm(tt)
            except Exception:
                speak("Sorry sir, I am unable to set the alarm.")


        elif intent_class == "jokes":
            joke = pyjokes.get_joke()
            speak(joke)


        elif intent_class == "switch_window":
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")


        elif intent_class == "news":
            try:
                speak("Please wait sir while I fetch the latest news.")
                news()
            except Exception:
                speak("Sorry sir, I could not fetch the news.")


        elif intent_class == "location":
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f"We are in {city}, {country}")
            except Exception as e:
                speak(" Sorry sir, I am unable to trace our location.")
                pass



        elif intent_class == "profile_instagram":
            try:
                speak(" Enter the username of the profile: ")
                name = input("Username")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Here is the profile of the user {name}")
                # time.sleep(5)
                '''speak("Would you like to download the profile picture of the account?")
                condition = takecommand().lower()
                if "yes" in condition:
                    mod = instaloader().Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("I am done sir. Profile picture has been downloaded successfully.")
                else:
                    pass'''
            except Exception:
                speak("Sorry sir, I am unable to perform the task.")



        elif intent_class == "screenshot":
            try:
                speak("What will be the file name of this screenshot")
                name = takecommand()
                speak("Please hold on the screen while I am taking the screenshot")
                img = pyautogui.screenshot()
                file_path = f"C:/Users/dipro/OneDrive/Desktop/Code Editor/Upgradation 2.0/Screenshot/{name}.png"
                img.save(file_path)
                speak("The file has been saved successfully.")
            except Exception:
                speak("Sorry sir, I am unable to take the screenshot.")


        elif intent_class == "read_pdf":
            name=input()
            pdf_reader(name)


        elif intent_class == "calculation":
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("What do you want to calculate?")
                    print("Listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)

                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'x': operator.mul,
                        '/': operator.__truediv__,
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)

                speak("The result is: ")
                speak(eval_binary_expr(*(my_string.split())))
            except Exception:
                speak("Sorry sir, I am unable to process the task.")


        elif intent_class == "twitterbot":
            email, password, verify = account_info()
            #speak("What do you want to tweet sir?")
            tweet = takecommand()
            option = Options()
            option.add_argument("start-maximized")
            driver = webdriver.Chrome(options=option)

            driver.get("https://twitter.com/login")
            time.sleep(2)


            email_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
            next_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
            verify_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
            verify_next_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div'
            password_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
            login_xpath = '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div'

            driver.find_element(by=By.XPATH,value=email_xpath).send_keys(email)
            time.sleep(1)
            driver.find_element(by=By.XPATH,value=next_xpath).click()
            time.sleep(2)
            
            driver.find_element(by=By.XPATH,value=verify_xpath).send_keys(verify)
            time.sleep(1)
            driver.find_element(by=By.XPATH,value=verify_next_xpath).click()
            time.sleep(1)
            
            driver.find_element(by=By.XPATH,value=password_xpath).send_keys(password)
            time.sleep(1)
            driver.find_element(by=By.XPATH,value=login_xpath).click()
            time.sleep(5)


            tweet_xpath = '/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div'
            message_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div'
            post_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/div[4]/div/span/span'

            time.sleep(4)

            driver.find_element(by=By.XPATH,value=tweet_xpath).click()
            time.sleep(1)
            driver.find_element(by=By.XPATH,value=message_xpath).send_keys(tweet)
            time.sleep(1)
            driver.find_element(by=By.XPATH,value=post_xpath).click()
            time.sleep(1)
            keyboard.press_and_release('ctrl + w')
            #time.sleep(60)
            
        elif intent_class == "temperature":
            try:
                speak("Of which place you want to find the temperature?")
                ques = takecommand()
                search = f"Temperature in {ques}"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"current {search} is {temp}")
            except Exception as e:
                speak("Sorry sir, I am unable to fetch the temperature.")



        elif intent_class == "how_to_do":
            speak("How to do mode is activated. ")
            while True:
                speak("Tell me what you want to know")
                how = takecommand()
                try:
                    if "exit" in how or "close" in how:
                        speak("How to do mode is closed")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak("Sorry sir, I am unable to find this.")


        elif intent_class == "battery":
            try:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Our system has {percentage} % power left.")
            except Exception:
                speak("Sorry sir, I am unable to check the battery percentage.")


        elif intent_class == "internet_speed" :
            try:
                st = spt.Speedtest()
                dl = st.download()
                dl = dl / 1000000
                rdl = round(dl, 2)
                up = st.upload()
                up = up / 1000000
                rup = round(up)
                speak(f"We have {rdl} MBPS downloading speed and {rup} MBPS uploading speed")
            except Exception:
                speak("Sorry sir, I am unable to check the internet speed.")


        elif intent_class == "volume_increase":
            try:
                pyautogui.press("volumeup")
            except Exception:
                speak("Sorry sir, I am unable to process the task.")


        elif intent_class == "volume_decrease":
            try:
                pyautogui.press("volumedown")
            except Exception:
                speak("Sorry sir, I am unable to process the task.")


        elif intent_class == "volume_mute":
            try:
                pyautogui.press("volumemute")
            except Exception:
                speak("Sorry sir, I am unable to process the task.")

        elif intent_class == "search":
            try:
                speak(" What do you want to search?")
                input_text = takecommand()
                answer = get_response(input_text = input_text)
               
                speak(answer)
            except:
                print("Sorry sir, I am unable to process the task.")

#        elif intent_class == "search":
#            try:
#                MainExecution()
#            except Exception:
#                speak("Sorry sir, I am unable to process the task.")

#        elif intent_class == "silence":
#            start()
        

        elif intent_class == "shut_down":
            os.system("shutdown -s")

        elif intent_class == "restart":
            os.system("shutdown -r")

        elif intent_class == "sleep":
            os.system("powercfg -hibernate on")

        elif intent_class == "hibernate":
            os.system("powercfg /hibernate on")

        else:
            analyzer = create_analyzer(task="sentiment", lang="en")
            sentiment_prediction = analyzer.predict(query)
            print(sentiment_prediction.output)
            if sentiment_prediction.output == "NEG":            
                intent_class = "negative_feedback"
                responses = intents[intent_class].get("responses")
                response = random.choice(responses)
                continue
        
            elif sentiment_prediction.output == "POS":
                intent_class = "positive_feedback"
                responses = intents[intent_class].get("responses")
                response = random.choice(responses)
                continue



def start():
    #opening_intent = ["hey candy", "wakeup", "wake up", "wakeup candy","wake up candy" "ok candy"]                   
    while True:
        query = takecommand()        
        response, intent_class = predict_intent(query)
        if intent_class == "start":
            speak(response)
            counter = True
            TaskExecution(counter)
            
start()

'''
def start():
    opening_intent = ["hey buddy", "wakeup", "wake up", "wakeup buddy","wake up buddy" "ok buddy"]                   
    while True:
        q = takecommand()
        if q in opening_intent:
            counter = True
            TaskExecution(counter)
            
start()

'''


'''
if __name__ == "__main__":
    if psutil.sensors_battery().percent <= 15:
        speak("We are low on battery. Please connect to charging.")

    


    recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
    recognizer.read('trainer/trainer.yml')  # load trained model
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)  # initializing haar cascade for object detection approach

    font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type

    id = 2  # number of persons you want to Recognize

    names = ['', 'Dipro']  # names, leave first empty bcz counter starts from 0

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
    cam.set(3, 640)  # set video FrameWidht
    cam.set(4, 480)  # set video FrameHeight

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    # flag = True

    while True:

        ret, img = cam.read()  # read the frames using the above created object

        converted_image = cv2.cvtColor(img,
                                       cv2.COLOR_BGR2GRAY)  # The function converts an input image from one color space to another

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # used to draw a rectangle on any image

            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])  # to predict on every single image


            # Check if accuracy is less them 100 ==> "0" is perfect match
            if (accuracy < 100):
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                cam.release()
                cv2.destroyAllWindows()
                speak("Access verified")
                start()
                





            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

'''