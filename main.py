import sys
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
from ultralytics import YOLO
import cv2
import numpy as np

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=3)
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            return command
    except sr.WaitTimeoutError:
        print("Listening timeout. Please speak something.")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please repeat.")
    except sr.RequestError:
        print("There was an error with the request to the speech recognition service.")
    return None


def run_assistant():
    try:
        command = take_command()
        if command:
            print("You said:", command)
            if 'play' in command:
                song = command.replace('play', '')
                talk('Playing ' + song)
                pywhatkit.playonyt(song)
            elif 'day' in command:
                today = datetime.date.today().strftime('%A')
                talk("Today is " + today)
            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                talk('The current time is ' + current_time)
            elif 'who is' in command:
                person = command.replace('who is ', '')
                info = wikipedia.summary(person, sentences=1)
                print(info)
                talk(info)
            elif 'date' in command:
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                talk('Today is ' + current_date)
            elif 'joke' in command:
                talk(pyjokes.get_joke())
            elif 'sketch' in command:
                talk('making your sketch')

                def sketch(image):
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    blur_gray = cv2.GaussianBlur(gray, (5, 5), 900)
                    edges = cv2.Canny(blur_gray, 45, 90)
                    ret, thre = cv2.threshold(edges, 70, 255, cv2.THRESH_BINARY_INV)
                    return thre

                cam = cv2.VideoCapture(0)

                while 1:
                    ret, frame = cam.read()
                    cv2.imshow('Live Sketch', sketch(frame))
                    if cv2.waitKey(1) == 27:
                        break
                    if cv2.waitKey(1) == 13:
                        cv2.imwrite('sketch.jpg', sketch(frame))
                        print('Image Saved!!!')

                cam.release()
            elif 'detect' in command:
                model = YOLO('yolov8n.pt')
                cap = model.predict(source='0', show=True)
            elif 'game' in command:
                import random

                # Generate a random number between 1 and 100
                secret_number = random.randint(1, 100)

                # Initialize the number of guesses
                guesses = 0

                talk('Welcome to the Guessing Game!')
                talk('I am thinking of a number between 1 and 100.')

                while True:
                    try:
                        # Get the player's guess
                        guess = int(input("Take a guess: "))
                        guesses += 1

                        # Check if the guess is correct
                        if guess == secret_number:
                            print(f"Congratulations! You guessed the number in {guesses} guesses.")
                            break
                        elif guess < secret_number:
                            print("Too low. Try again.")
                        else:
                            print("Too high. Try again.")
                    except ValueError:
                        print("Please enter a valid number.")

            elif 'quit' in command:
                talk('Goodbye!')
                sys.exit()
            else:
                talk('I did not understand your command. Please try again.')
    except Exception as e:
        print("An error occurred:", str(e))
        talk("Sorry, an error occurred.")


if __name__ == "__main__":
    while True:
        run_assistant()
