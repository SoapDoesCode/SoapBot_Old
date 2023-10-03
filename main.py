from neuralintents.assistants import BasicAssistant # pip install neuralintents
from dotenv import load_dotenv # pip install python-dotenv
import speech_recognition as sr # pip install SpeechRecognition
import pygame # pip install pygame
import pyttsx3 # pip install pyttsx3
import requests # pip install requests
import wikipedia # pip install wikipedia
from googletrans import Translator # pip install googletrans==3.1.0a0

import webbrowser
from configparser import ConfigParser
import time
import datetime
import os
import sys
import json
import math
import random

# Use "python -m pip install --upgrade pip" first to upgrade pip then,
# Use "pip install -r requirements.txt" to install requirements


# 1000 epochs = loss: 1.1280 - accuracy: 0.7685
# 200 epochs = loss: 1.8953 - accuracy: 0.8408
# 100 epochs = loss: 0.9821 - accuracy: 0.8623
# 90 epochs = loss: 0.8942 - accuracy: 0.8635
# 80 epochs = loss: 0.8259 - accuracy: 0.8598
# 70 epochs = loss: 0.8965 - accuracy: 0.8553
# 60 epochs = loss: 0.7402 - accuracy: 0.8595
# 50 epochs = loss: 0.7852 - accuracy: 0.8642
# 40 epochs = loss: 0.7344 - accuracy: 0.8645 # Best numebr of epochs for my intents.json
# 30 epochs = loss: 0.8074 - accuracy: 0.8540
# 20 epochs = loss: 0.7514 - accuracy: 0.8619
# 10 epochs = loss: 0.7767 - accuracy: 0.8420
# 5 epochs = loss: 0.8324 - accuracy: 0.8300

epoch_count = 40 # Set the number of epochs to be trained on

# Variables Start
load_dotenv() # Load the .env file

config = ConfigParser()
config.read("config.ini")
# config.add_section('settings')
# config.set('settings', 'key1', 'value1')
# config.set('settings', 'key2', 'value2')
# config.set('settings', 'key3', 'value3')
# with open('config.ini', 'w') as f:
#     config.write(f)

ChatbotName = (config.get('settings', 'Chatbot_Name')) # -> "value1"
WakeWord = (config.get('settings', 'Wake_Word')) # -> "value2"
PlayStartSound = (config.getboolean('settings', 'Play_Start_Sound')) # -> "value3"
TrainResponses = (config.getboolean('settings', 'Train_Responses')) # -> "value4"

engine = pyttsx3.init() # Initialize pyttsx3

# r = sr.Recognizer() # Initialize speech recognition

# weather variables
city = "Lichfield"
units = "metric"
weather_api_key = os.getenv("WEATHER_API_KEY")
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={weather_api_key}"
# Variables Stop

# Startup Sound
# if PlayStartSound == True:
#     pygame.mixer.init()
#     pygame.mixer.music.load("sound_effects/Startup_Song.mp3")
#     pygame.mixer.music.play()
# Startup Sound

def settings():
    print("Nothing here yet")

# Functions Start

def bot_say(text):
    if text != None:
        print(f"{ChatbotName}: {text}")
        engine.say(text)
        engine.runAndWait()

def function_for_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    bot_say(f"The current time is {current_time}")

def function_for_date():
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    current_date = str(current_date) # Converts the date to a string
    current_day = datetime.datetime.now().strftime("%A")
    current_day = str(current_day) # Converts the day to a string
    bot_say(f"It is {current_day} {current_date}")

def function_for_weather():
    if weather_api_key == "" or weather_api_key == None:
        bot_say("Sorry, I don't have a weather API key, please add one to the .env file!")
        return
    response = requests.get(weather_url)
    if response.status_code == 200:
        weather_data = json.loads(response.text)
        weather = weather_data["weather"][0]["main"]
        # replace "clouds" with "cloudy" and "clear" with "the sky is clear" for better grammar
        if weather == "Clouds":
            weather = "cloudy"
        elif weather == "Clear":
            weather = "ckear skies"
        temperature = weather_data["main"]["temp"]
        temperature = math.floor(temperature) # Rounds the temperature down to the nearest whole number
        bot_say(f"The temperature in {city} is {temperature}°C and {weather}")

def function_for_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        joke_data = json.loads(response.text)
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        bot_say(f"{setup} {punchline}")
    else:
        bot_say("Sorry, I couldn't find a joke :(")

def function_for_riddle():
    riddleRequest = requests.get("https://ibk-riddles-api.herokuapp.com/")
    json_data = json.loads(riddleRequest.text)
    Question = json_data["question"]
    Answer = json_data["answer"]
    bot_say(f"The question is: {Question}")
    input("Guess: ")
    bot_say(f"The answer is: {Answer}")

def function_for_wikipedia():
    bot_say("What would you like to search on Wikipedia?")
    search = input("Search: ")
    wikiURL = wikipedia.wikipedia.page(search).url
    bot_say(f"Searching Wikipedia for {search}")
    try:
        results_1 = wikipedia.summary(search, sentences=2)
        bot_say(results_1)
        bot_say("Would you like to know more?") # ask the user if they would like to know more
        answer = input("Answer: ")
        if "yes" in answer:
            results = wikipedia.summary(search, sentences=5) # remove the any sentences that have already been said
            results = results.replace(f"{results_1}", "")
            bot_say(results) # ask the user if they would like to open the wikipedia page
            bot_say("Would you like to open the Wikipedia page?")
            answer = input("Answer: ")
            if "yes" in answer:
                webbrowser.open(wikiURL)
                bot_say("Opening the Wikipedia page")
            else:
                bot_say("Okay, no problem")
        else:
            bot_say("Would you like to open the Wikipedia page?") # ask the user if they would like to open the wikipedia page
            answer = input("Answer: ")
            if "yes" in answer:
                webbrowser.open(wikiURL)
                bot_say("Opening the Wikipedia page")
            else:
                bot_say("Okay, no problem")
    except wikipedia.exceptions.DisambiguationError as e:
        bot_say("Sorry, I couldn't find that on Wikipedia")
        bot_say("Here are some results that I found")
        bot_say(e.options)
    except:
        bot_say("Sorry, I couldn't find anything on Wikipedia")

def function_for_google():
    googleURL = "https://www.google.com/"
    if "search" in message:
        bot_say("What would you like to search on Google?")
        search = input("Search: ")
        webbrowser.open(f"{googleURL}search?q={search}")
        bot_say(f"Searching Google for {search}")
    else:
        webbrowser.open(googleURL)
        bot_say("Opening Google...")

def function_for_youtube():
    youtubeURL = "https://www.youtube.com/"
    if "search" in message:
        bot_say("What would you like to search for?")
        search = input("Search: ")
        youtubeURL = f"{youtubeURL}results?search_query={search}"
        webbrowser.open(youtubeURL)
        bot_say(f"Searching YouTube for {search}")
    else:
        webbrowser.open(youtubeURL)
        bot_say("Opening the YouTube homepage")

def function_for_twitter():
    twitterURL = "https://twitter.com/"
    if "search" in message:
        bot_say("What would you like to search on Twitter?")
        search = input("Search: ")
        twitterURL = f"{twitterURL}search?q={search}"
        webbrowser.open(twitterURL)
        bot_say(f"Searching Twitter for {search}")
    else:
        webbrowser.open(twitterURL)
        bot_say("Opening the Twitter homepage")

def function_for_instagram():
    instagramURL = "https://www.instagram.com/"
    webbrowser.open(instagramURL)
    bot_say("Opening Instagram")

def function_for_facebook():
    facebookURL = "https://www.facebook.com/"
    webbrowser.open(facebookURL)
    bot_say("Opening Facebook...")

def function_for_tiktok():
    tiktokURL = "https://www.tiktok.com/"
    webbrowser.open(tiktokURL)
    bot_say("Opening TikTok...")

def function_for_reddit():
    redditURL = "https://www.reddit.com/"
    if "search" in message:
        bot_say("What subreddit would you like to search for?")
        search = input("Search: ")
        redditURL = f"{redditURL}search/?q={search}&type=sr"
        webbrowser.open(redditURL)
        bot_say(f"Searching Reddit for {search}")
    else:
        webbrowser.open(redditURL)
        bot_say("Opening Reddit...")

def function_for_spotify():
    spotifyURL = "https://open.spotify.com/"
    possibleSearches = ["search", "play", "find", "listen", "song", "artist", "album", "playlist", "podcast"]
    if any(possible in message.lower() for possible in possibleSearches):
        bot_say("What would you like to search for?")
        search = input("Search: ")
        spotifyURL = f"{spotifyURL}search/{search}"
        webbrowser.open(spotifyURL)
        bot_say(f"Searching Spotify for {search}")
    else:
        webbrowser.open(spotifyURL)
        bot_say("Opening Spotify...")

def function_for_netflix():
    netflixURL = "https://www.netflix.com/"
    possibleSearches = ["search", "play", "find", "watch", "movie", "show", "tv", "series", "episode"]
    if any(possible in message.lower() for possible in possibleSearches):
        bot_say("What would you like to search for on Netflix?")
        search = input("Search: ")
        netflixURL = f"{netflixURL}search?q={search}"
        webbrowser.open(netflixURL)
        bot_say(f"Searching Netflix for {search}")
    else:
        bot_say("Opening Netflix...")
        webbrowser.open(netflixURL)

def function_for_amazon():
    amazonURL = "https://www.amazon.com/"
    possibleSearches = ["search", "find", "buy", "product", "item", "shop"]
    if any(possible in message.lower() for possible in possibleSearches):
        bot_say("What would you like to search for on Amazon?")
        search = input("Search: ")
        amazonURL = f"{amazonURL}s?k={search}"
        webbrowser.open(amazonURL)
        bot_say(f"Searching Amazon for {search}")
    else:
        webbrowser.open(amazonURL)
        bot_say("Opening Amazon...")

def function_for_ebay():
    ebayURL = "https://www.ebay.com/"
    possibleSearches = ["search", "find", "buy", "product", "item", "shop"]
    if any(possible in message.lower() for possible in possibleSearches):
        bot_say("What would you like to search for on eBay?")
        search = input("Search: ")
        ebayURL = f"{ebayURL}sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={search}&_sacat=0"
        webbrowser.open(ebayURL)
        bot_say(f"Searching eBay for {search}")
    else:
        webbrowser.open(ebayURL)
        bot_say("Opening eBay...")

def function_for_outlook():
    outlookURL = "https://outlook.live.com/mail/0/inbox"
    webbrowser.open(outlookURL)
    bot_say("Opening Outlook...")

def function_for_discord():
    discordURL = "https://discord.com/channels/@me"
    webbrowser.open(discordURL)
    bot_say("Opening Discord...")

def function_for_whatsapp():
    whatsappURL = "https://web.whatsapp.com/"
    webbrowser.open(whatsappURL)
    bot_say("Opening WhatsApp...")

# do not add a function for skype, gmail or slack because i don't use it

def function_for_teams():
    teamsURL = "https://teams.microsoft.com/"
    webbrowser.open(teamsURL)
    bot_say("Opening Microsoft Teams...")

def function_for_github():
    githubURL = "github.com/"
    webbrowser.open(githubURL)
    bot_say("Opening GitHub...")

def function_for_stackoverflow():
    stackoverflowURL = "https://stackoverflow.com/"
    webbrowser.open(stackoverflowURL)
    bot_say("Opening Stack Overflow...")

def function_for_thingiverse():
    thingiverseURL = "https://www.thingiverse.com/"
    webbrowser.open(thingiverseURL)
    bot_say("Opening Thingiverse...")

def function_for_cults3d():
    cults3dURL = "https://cults3d.com/en"
    webbrowser.open(cults3dURL)
    bot_say("Opening Cults3D...")

def function_for_games():
    print("Nothing here yet")

def function_for_translate():
    bot_say("What would you like to translate?")
    translate = input("Translate: ")
    bot_say("What language would you like to translate to?")
    language = input("Language: ")
    translator = Translator()
    translated = translator.translate(translate, dest=language)
    bot_say(f"'{translated.origin}' in {language} is '{translated.text}'")

def function_for_calculate():
    bot_say("What would you like to calculate?")
    calc = input("Calculate: ").lower()
    if "!" in calc or "factorial" in calc:
        calc = calc.replace("!", "")
        calc = calc.replace("factorial", "")
        calc = int(calc)
        bot_say(f"The factorial of {calc} is {math.factorial(calc)}")
        return
    char_to_replace = {"plus": "+", "add": "+", "minus": "-", "take away": "-", "times": "*", "divided by": "/", "over": "/", "to the power of": "**", "squared": "**2", "cubed": "**3", "pi": "3.14", "of": ""}
    for char in char_to_replace:
        calc = calc.replace(char, char_to_replace[char])
    try:
        bot_say(f"The answer is {eval(calc)}")
    except:
        bot_say("I don't know how to calculate that, sorry.")

def function_for_insult():
    insultURL = "https://evilinsult.com/generate_insult.php?lang=en&type=text"
    insult = requests.get(insultURL).text
    bot_say(insult)

def function_for_compliment():
    complimentURL = "https://complimentr.com/api"
    compliment = requests.get(complimentURL).json()
    compliment = compliment["compliment"][0].upper() + compliment["compliment"][1:]
    bot_say(compliment)

def function_for_quote():
    quoteURL = "https://api.quotable.io/random"
    quote = requests.get(quoteURL).json()
    bot_say(f"{quote['content']} - {quote['author']}")

def function_for_fact():
    factURL = "https://uselessfacts.jsph.pl/random.json?language=en"
    fact = requests.get(factURL).json()
    bot_say(fact["text"])

def function_for_help():
    bot_say("Here are the commands I can do:")
    bot_say(", ".join(mappings.keys()))

# Functions Stop

mappings = {"time" : function_for_time, # Create a dictionary of functions
            "date" : function_for_date,
            "weather" : function_for_weather,
            "joke" : function_for_joke,
            "riddle" : function_for_riddle,
            "wikipedia" : function_for_wikipedia,
            "google" : function_for_google,
            "youtube" : function_for_youtube,
            "twitter" : function_for_twitter,
            "instagram" : function_for_instagram,
            "facebook" : function_for_facebook,
            "tiktok" : function_for_tiktok,
            "reddit" : function_for_reddit,
            "spotify" : function_for_spotify,
            "netflix" : function_for_netflix,
            "amazon" : function_for_amazon,
            "ebay" : function_for_ebay,
            "outlook" : function_for_outlook,
            "discord" : function_for_discord,
            "whatsapp" : function_for_whatsapp,
            "teams" : function_for_teams,
            "github" : function_for_github,
            "stackoverflow" : function_for_stackoverflow,
            "thingiverse" : function_for_thingiverse,
            "cults3d" : function_for_cults3d,
            "games" : function_for_games,
            "translate" : function_for_translate,
            "calculate" : function_for_calculate,
            "help" : function_for_help,
            "insult" : function_for_insult,
            "compliment" : function_for_compliment,
            "quote" : function_for_quote,
            "fact" : function_for_fact}

chatbot = BasicAssistant('intents.json', model_name=ChatbotName) # Load the intents.json file
if TrainResponses == True:
    chatbot.fit_model(epochs=epoch_count) # Train the chatbot
    chatbot.save_model() # Save the chatbot
    config.set('settings', 'Train_Responses', 'False') # Set Train_Responses to False once the chatbot has been trained
    with open('config.ini', 'w') as configfile:
        config.write(configfile) # Update the config file
else:
    chatbot.load_model()
# The chatbot is now initialized

done = False # Set done to False

startupMessage = f"{ChatbotName} is online and working... probably :P"
print(startupMessage)
engine.say(startupMessage)
engine.runAndWait()
bot_say(f"The wake word is {WakeWord}")

while not done: # While done is False
    global message
    message = input("You: ") # Get the user's input
    message = message.lower().replace(WakeWord, "") # Make the message lowercase and remove the wake word
    exitMessages = ["exit", "quit", "stop", "shutdown", "turn off"]
    if any(exit in message.lower() for exit in exitMessages): # If the message contains any of the exit messages
        sys.exit() # Exit the program
    elif message.lower() == "":
        pass
    else:
        try:
            mappings[message]()
            pass
        except KeyError: # If there is no function for the message, run the chatbot
            response = chatbot.process_input(message)
            bot_say(response)
            message = ""