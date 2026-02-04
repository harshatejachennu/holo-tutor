import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import urllib.parse

def fetch_first_image(keyword):
    query = urllib.parse.quote(keyword)
    url = f"https://www.google.com/search?tbm=isch&q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all("img")

    for img in img_tags:
        img_url = img.get("src")
        if img_url and img_url.startswith("http"):
            print(f"🖼️ Found image URL: {img_url}")
            return img_url
    print("❌ No valid image found.")
    return None

def download_and_flip_image(img_url, output_path='hologram_image.jpg'):
    response = requests.get(img_url)
    image = Image.open(BytesIO(response.content))

    # Convert palette images (mode 'P') to RGB for JPEG saving
    if image.mode == 'P':
        image = image.convert('RGB')

    # Flip vertically for Pepper's Ghost (adjust if needed)
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    flipped_image.save(output_path)
    print(f"✅ Hologram-ready image saved to {output_path}")

if __name__ == "__main__":
    keyword = input("Enter a visual keyword to search for an image: ")
    img_url = fetch_first_image(keyword)

    if img_url:
        download_and_flip_image(img_url)
