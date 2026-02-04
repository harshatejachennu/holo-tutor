from speech_to_text import transcribe_speech
from query_gpt import query_gpt
from text_to_speech import speak_text

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import urllib.parse
import os
import socket
import threading
import http.server
import socketserver
import qrcode
import webbrowser

PORT = 8000
HOLOGRAM_IMAGE = 'hologram_image.jpg'

# --- Utility: Get Local IP ---
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# --- Start HTTP Server in Background ---
def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🌐 Serving at http://{get_local_ip()}:{PORT}")
        httpd.serve_forever()

def serve_image():
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()

# --- Fetch, Flip, Save Image ---
def search_and_prepare_image(keyword, output_path=HOLOGRAM_IMAGE):
    print(f"🔍 Searching image for: {keyword}")
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all("img")

    for img in img_tags:
        img_url = img.get("src")
        if img_url and img_url.startswith("http"):
            print(f"🖼️ Found image URL: {img_url}")
            response_img = requests.get(img_url)
            image = Image.open(BytesIO(response_img.content))
            if image.mode == 'P':
                image = image.convert('RGB')
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            flipped_image.save(output_path)
            print(f"✅ Hologram-ready image saved to {output_path}")
            return True

    print("❌ No valid image found.")
    return False

# --- Generate QR Code ---
def make_qr(ip, port=PORT, filename='qr.png'):
    url = f"http://{ip}:{port}/{HOLOGRAM_IMAGE}"
    img = qrcode.make(url)
    img.save(filename)
    print(f"📱 QR code generated: {filename} (Scan with iPhone to view)")
    webbrowser.open(f"file://{os.path.abspath(filename)}")  # Opens QR code on Mac

def holo_tutor_session():
    serve_image()

    print("🎤 Speak your question now:")
    user_question = transcribe_speech()
    if not user_question:
        print("❌ No input detected. Try again.")
        return

    print(f"📝 You asked: {user_question}")

    explanation, visual_keyword = query_gpt(user_question)

    if explanation:
        print(f"\n🗣️ Explanation: {explanation}")
        speak_text(explanation)
    else:
        print("❌ Could not get an explanation from the AI.")

    if visual_keyword:
        print(f"🖼️ Visual Keyword Suggestion: {visual_keyword}")
        success = search_and_prepare_image(visual_keyword)
        if success:
            ip = get_local_ip()
            make_qr(ip)
            print(f"👉 Open on iPhone: http://{ip}:{PORT}/{HOLOGRAM_IMAGE}")
    else:
        print("❌ No visual keyword provided.")

if __name__ == "__main__":
    holo_tutor_session()

import time

if __name__ == "__main__":
    holo_tutor_session()
    print("🟢 Holo-Tutor session complete. Server is still running. Press CTRL+C to stop.")
    while True:
        time.sleep(1)
