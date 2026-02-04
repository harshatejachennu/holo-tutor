import requests
import json

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemma-3-27b-it:free"

def query_gpt(user_input):
    prompt = f"""
You are Holo-Tutor, a concise study assistant for students. When given a question, provide:
1. A brief, spoken-friendly explanation of the topic.
2. A short search keyword or phrase that could find a relevant diagram, image, or visual aid.

Return the output in this format:
Explanation: <explanation here>
VisualKeyword: <keyword for visual search>

Question: {user_input}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Holo-Tutor"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 300
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code} - {response.text}")
        return None, None

    reply = response.json()['choices'][0]['message']['content']
    print("📘 Gemma Response:\n", reply)

    # Parse explanation and visual keyword
    explanation, visual_keyword = None, None
    lines = reply.split('\n')
    for line in lines:
        if line.startswith("Explanation:"):
            explanation = line.replace("Explanation:", "").strip()
        elif line.startswith("VisualKeyword:"):
            visual_keyword = line.replace("VisualKeyword:", "").strip()

    return explanation, visual_keyword


if __name__ == "__main__":
    user_question = input("Enter your question for Holo-Tutor: ")
    explanation, visual_keyword = query_gpt(user_question)

    print(f"\n🗣️ Explanation: {explanation}")
    print(f"🖼️ Visual Keyword: {visual_keyword}")
