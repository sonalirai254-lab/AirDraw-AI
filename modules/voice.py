import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(source)

        print("Listening...")

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print(text)

        return text.lower()

    except:

        return ""