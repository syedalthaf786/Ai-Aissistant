import os
import datetime
import webbrowser
import pyjokes
import pywhatkit
import pyautogui
import wikipedia
import pyttsx3
import speech_recognition as sr

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 200)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
voices = engine.getProperty('voices')
for voice in voices:
    print(f"ID: {voice.id}, Name: {voice.name}")

# Select the Microsoft Zira voice
female_voice_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'
engine.setProperty('voice', female_voice_id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        
        # Optional: Save audio to a file for debugging
        with open("output.wav", "wb") as f:
            f.write(audio.get_wav_data())
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            talk("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            talk(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def greeting():
    current_time = datetime.datetime.now()
    hour = current_time.hour
    if 3 <= hour < 12:
        talk("Good morning, sir.")
    elif 12 <= hour < 18:
        talk("Good afternoon, sir.")
    else:
        talk("Good evening, sir.")

def run_jenny():
    query = take_command()
    
    if 'hello' in query:
        talk("Hi boss, how are you?")
    
    elif 'joke' in query:
        talk(pyjokes.get_joke())
    
    elif 'sleep' in query:
        talk("Goodbye")
        exit()
    
    elif 'play' in query:
        song = query.replace('play', '').strip()
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)
    
    elif 'time' in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        print(time)
        talk(f"Current time: {time}")
    
    elif 'open' in query:
        app = query.replace('open', '').strip()
        pyautogui.press('super')
        pyautogui.typewrite(app)
        pyautogui.sleep(1)
        pyautogui.press('enter')
        talk(f'Opening {app}')
    
    elif 'close' in query:
        pyautogui.hotkey('alt', 'f4')
        talk("Closing sir")
    
    elif 'who is' in query:
        person = query.replace('who is', '').strip()
        info = wikipedia.summary(person, sentences=1)
        print(info)
        talk(info)
    
    elif 'remember that' in query:
        remember_msg = query.replace('remember that', '').strip()
        talk(f"You told me to remember that {remember_msg}")
        with open('remember.txt', 'a') as remember_file:
            remember_file.write(remember_msg + "\n")
    
    elif 'what do you remember' in query:
        try:
            with open('remember.txt', 'r') as remember_file:
                memories = remember_file.read()
            talk(f"You told me to remember: {memories}")
        except FileNotFoundError:
            talk("I don't have anything to remember.")
    
    elif 'clear remember file' in query:
        with open('remember.txt', 'w') as remember_file:
            remember_file.write('')
        talk("Done sir! Everything I remembered has been deleted.")
    
    elif 'shutdown' in query:
        talk("Shutting down the PC in 3... 2... 1...")
        os.system('shutdown /s /t 1')
    
    elif 'restart' in query:
        talk("Restarting the PC in 3... 2... 1...")
        os.system('shutdown /r /t 1')
    
    elif 'search' in query:
        search_term = query.replace('search', '').strip()
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        talk("This is what I found on the internet.")
    
    elif 'stop' in query or 'start' in query:
        pyautogui.press('k')
        talk("Done sir!")
    
    elif 'full screen' in query:
        pyautogui.press('f')
        talk("Done sir!")
    
    elif 'theater screen' in query:
        pyautogui.press('t')
        talk("Done sir!")
    
    elif 'i love you' in query:
        talk("Love you too, sir")
    
    
    # else:
        # talk("I don't understand")

if __name__ == "__main__":
    greeting()
    talk('My name is Jenny.')
    talk("Say something, sir.")
    while True:
        run_jenny()
