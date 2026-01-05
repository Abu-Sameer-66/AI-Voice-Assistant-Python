import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
import os
import sys  # Needed to exit the program cleanly

# --- Engine Setup ---
# Using pyttsx3 for offline TTS because it's faster than waiting for API calls
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Adjust voice rate (optional, standard is usually too fast)
engine.setProperty('rate', 170) 

# --- CONFIGURATION SECTION ---
# TODO: Move these to environment variables for production (Safety First!)
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE" 
NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"

def speak(text):
    """
    Speaks the text and also prints it to console for debugging.
    """
    print(f"Check: {text}")  # Visual log for the developer
    engine.say(text)
    engine.runAndWait()

def ask_gpt(query):
    """
    Sends complex queries to GPT-3.5 when local logic can't handle it.
    """
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis, a smart coding assistant. Keep answers brief and technical."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error connecting to OpenAI: {e}")
        return "Sorry, I lost connection to the brain."

def execute_command(command):
    """
    Main logic controller. Filters specific commands before calling AI.
    """
    command = command.lower()
    
    # 1. Web Navigation
    if "open google" in command:
        speak("Opening Google...")
        webbrowser.open("https://google.com")
    
    elif "open youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://youtube.com")
    
    # 2. Music Player (Local Library)
    elif command.startswith("play"):
        try:
            # Expected command: "Play heer"
            song_name = command.split(" ")[1] 
            link = musiclibrary.music[song_name]
            speak(f"Playing {song_name} from your library.")
            webbrowser.open(link)
        except KeyError:
            speak("That song isn't in your music library. Check musiclibrary.py")
        except IndexError:
            speak("Please specify a song name.")

    # 3. News Fetcher
    elif "news" in command:
        speak("Fetching latest headlines...")
        url = f"https://newsapi.org/v2/top-headlines?country=pk&apiKey={NEWS_API_KEY}"
        
        try:
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                articles = data.get('articles', [])[:5] # Get top 5 only
                
                for i, article in enumerate(articles):
                    speak(f"Headline {i+1}: {article['title']}")
            else:
                speak("News API is currently down.")
        except Exception as e:
            print(f"Network Error: {e}")
            speak("I need internet to check the news.")

    # 4. System Control
    elif "exit" in command or "quit" in command:
        speak("Shutting down. Goodbye Sameer.")
        sys.exit()

    # 5. Fallback to AI
    else:
        print("Command not recognized locally, asking GPT...")
        reply = ask_gpt(command)
        speak(reply)

# --- Entry Point ---
if __name__ == "__main__":
    print("--- JARVIS SYSTEM ONLINE ---")
    speak("System Online. Waiting for wake word.")
    
    while True:
        try:
            # Listen for Wake Word first to save resources
            with sr.Microphone() as source:
                print("\nListening for 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5) # Fixes background noise issues
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            
            try:
                word = recognizer.recognize_google(audio)
                
                if "jarvis" in word.lower():
                    speak("Active.")
                    
                    # Wake word detected, now listen for command
                    with sr.Microphone() as source:
                        print(">> Waiting for command...")
                        # Increase timeout so user has time to think
                        audio_cmd = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        
                        user_command = recognizer.recognize_google(audio_cmd)
                        print(f"User said: '{user_command}'")
                        execute_command(user_command)
                        
            except sr.UnknownValueError:
                pass # Silence is golden. Don't spam console if no speech.
            except sr.RequestError:
                speak("Network error. Check your internet.")
                
        except Exception as e:
            # Catch-all to prevent crash loop
            print(f"System Error: {e}")
