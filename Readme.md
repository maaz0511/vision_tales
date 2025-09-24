# VisionTales 🎨📖🔊

**Where your pictures come alive as stories.**

VisionTales is an AI-powered storytelling web app built with **Streamlit**.
Upload 1–10 images, choose a story style and language — and let AI craft a unique narrative and narrate it back to you.

---

## ✨ Features

* 📸 **Image to Story** – Upload up to 10 images and generate a connected narrative.
* 🎭 **Story Styles** – Comedy, Thriller, Fairy Tale, Sci-Fi, Mystery, Adventure, and Morale.
* 🌍 **Language Support** – Generate stories in any supported language (e.g., English, Hindi, Tamil).
* 🗣️ **Narration** – Listen to your story with AI-generated audio (powered by gTTS).
* ⚡ **Powered by Google Gemini** – Uses Google’s generative AI for text understanding and story generation.

---

## 🚀 Demo

![Demo Screenshot](demo.png)
*(Add your app screenshot here)*

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/visiontales.git
cd visiontales
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root folder and add your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
visiontales/
│── app.py                # Streamlit UI
│── story_generator.py    # AI logic for story & audio
│── requirements.txt      # Dependencies
│── .env.example          # Example env file
```

---

## ⚙️ Tech Stack

* [Streamlit](https://streamlit.io/) – Web UI
* [Google Generative AI](https://ai.google.dev/) – Story generation
* [gTTS](https://pypi.org/project/gTTS/) – Text-to-speech
* [Pillow](https://pillow.readthedocs.io/) – Image handling
* [Python dotenv](https://pypi.org/project/python-dotenv/) – Environment management

---

## 🎯 Usage

1. Upload **1–10 images**.
2. Select a **story style**.
3. Enter your **language code** (e.g., `en`, `hi`, `ta`).
4. Click **Generate Story**.
5. Read the story and listen to the narration (`.mp3` playback in-app).

---

## ⚠️ Notes

* API key from **Google AI Studio** is required.
* Narration output is generated in `.mp3` format and played via Streamlit audio.
* Max upload size: **10 images**.

---

## 🖼️ Example Output

**Story (Fairy Tale, Hindi):**

```
शीर्षक: जादुई जंगल का रहस्य
...
```

**Narration:**
🔊 AI-generated audio playback inside the app.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and submit PRs.

---

## 👨‍💻 Author

* Developed by Mohd Maaz
