Holo-Tutor — AI Hologram Study Assistant

This is a personal project where I built a voice-controlled study assistant that explains concepts out loud and shows supporting visuals as a “hologram” using a Pepper’s Ghost-style projection setup (phone + plexiglass + bell jar).

The idea was to make studying more interactive. Instead of just asking an AI for an answer, you can speak a question, hear the explanation, and see a floating visual at the same time.

I built this to experiment with AI APIs, speech recognition, image processing, and a simple physical projection system.

What It Does

Takes a spoken question through the laptop mic

Converts speech → text

Sends the question to an AI model for explanation

Reads the explanation out loud

Finds a related diagram/image

Flips the image for Pepper’s Ghost optics

Serves the image to an iPhone viewer page

Displays it in a hologram-style projection setup

Example Use

Say:

“What is the quadratic formula?”

The system will:

explain it out loud

fetch a formula diagram

format it for hologram reflection

display it on the phone viewer page

project it inside the jar setup

Tech Used

Python

SpeechRecognition

Text-to-speech (macOS say)

Requests + web scraping

Pillow (image processing/flipping)

Simple local HTTP server

HTML auto-refresh viewer page

AI model API (via OpenRouter)

Files

Main pieces:

HoloTutorFull.py — main pipeline runner

speech_to_text.py — mic input

query_gpt.py — AI query + parsing

text_to_speech.py — spoken output

hologram_image.py — image fetch + flip

index.html — iPhone viewer page

How To Run
source holo-tutor-env/bin/activate
python HoloTutorFull.py


Then open the viewer page on your phone (same Wi-Fi):

http://<your-mac-ip>:8000

Hardware Setup

iPhone screen as a projection source

angled plexiglass reflector

glass bell jar enclosure

single-view Pepper’s Ghost configuration

Limitations

Image quality depends on search results

Diagram selection is automatic, not curated

Works best on same Wi-Fi network

Built for single-viewer projection

Why I Built It

I wanted to try combining:

voice interfaces

AI explanations

visual learning

and a physical projection effect

into one working system instead of just a software demo.
