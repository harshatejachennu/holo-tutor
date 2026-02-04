import subprocess

def speak_text(text):
    if text:
        print(f"🔊 Speaking: {text}")
        subprocess.run(['say', text])
    else:
        print("❌ No text to speak.")

if __name__ == "__main__":
    sample_text = "This is a test of Holo-Tutor's speech system."
    speak_text(sample_text)