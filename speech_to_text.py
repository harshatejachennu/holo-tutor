import speech_recognition as sr

def transcribe_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("📝 Transcribing...")
        text = recognizer.recognize_google(audio)
        print(f"✅ Transcribed Text: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"❌ Could not request results; {e}")
        return None
