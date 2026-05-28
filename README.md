Audio to Text Converter (Whisper Max)



A clean, minimal, and modern desktop application to transcribe audio and video files into text locally on your computer using OpenAI's Whisper model. 100% private, secure, and offline-ready.



Key Features

Total Privacy: Runs completely locally. Your audio files are never uploaded to any cloud servers.

Live Monitoring: Watch the text appear in real-time as the AI processes the audio.

Smart Timestamps: Every line of text comes with precise time markings `\[00:00 --> 00:05]`.

Progress Bar: High-precision completion tracking based on the actual duration of the media file.

Control Buttons: Start or instantly Stop/Reset the process whenever you want.

Neutral Minimalist UI: A sleek, monochrome interface that perfectly matches dark and light OS themes.



How to Install \& Run (For Users)

1. Go to the \*\*Releases\*\* section on the right side of this GitHub page.

2. Download the latest `video\_to\_text.exe`.

3. Launch the app and select your audio/video file.



Note: On the very first run, the app will automatically download the Whisper ИИ model (\~460 MB) from official servers. Internet connection is required for the first transcription only. All future sessions work 100% offline.\*



evelopment & Manual Setup

If you want to run the source code directly:



1. Clone this repository.

2. Install the required dependencies:

```bash

&#x20;  pip install customtkinter whisper torch tinytag

