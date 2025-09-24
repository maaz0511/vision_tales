from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import wave
import io


load_dotenv()

# 1. load api key
api_key= os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise  ValueError("API key  not found")

# 2. create Client object
client= genai.Client(api_key=api_key)



# 3. create detailed prompt
def prompt(story_style:str, story_language:str)->str:
    """
    Build a storytelling prompt string for a generative AI model.

    This function creates a structured instruction template that guides
    the model to generate a story in a specific language and style.
    The prompt enforces constraints like connecting all images into a 
    coherent narrative, using Indian cultural context, and including 
    style-specific additions such as a moral, twist, or solution.

    Args:
        story_style (str): The narrative genre/style. Supported options are:
            - "Morale"   → Adds a [MORAL] section with the lesson.
            - "Mystery"  → Adds a [SOLUTION] section revealing the culprit.
            - "Thriller" → Adds a [TWIST] section with a shocking twist.
        story_language (str): The target language (BCP-47 code) in which
            the story should be written, e.g., "en", "hi", "ta".

    Returns:
        str: A formatted prompt string containing persona, goals,
        instructions, and style-specific requirements that can be
        passed directly to a text generation model.
    """

    base_prompt = f"""
    **Your Persona:** You are a friendly and engaging storyteller. Your goal is to tell a story that is fun and easy to read.
    **Your Main Goal:** Write a story in simple, clear, and modern **'{story_language}'** story_language.
    **Your Task:** Create one single story that connects all the provided images in order.
    **Style Requirement:** The story must fit the '{story_style}' genre.
    **Core Instructions:**
    1.  **Tell One Single Story:** Connect all images into a narrative with a beginning, middle, and end.
    2.  **Use Every Image:** Include a key detail from each image.
    3.  **Creative Interpretation:** Infer the relationships between the images.
    4.  **Nationality**: Use only Indian Names,Characters, Places , Persona Etc.
    **Output Format:**
    -   **Title:** Start with a simple and clear title.
    -   **Length:** The story must be between 4 and 5 paragraphs.
    -   **Language:** The output must in **'{story_language}'** story_language.
    """

    # --- Add Style-Specific Instructions ---
    style_instruction = ""
    if story_style == "Morale":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[MORAL]:` followed by the single-sentence moral of the story."
    elif story_style == "Mystery":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[SOLUTION]:` that reveals the culprit and the key clue."
    elif story_style == "Thriller":
        style_instruction = "\n**Special Section:** After the story, you MUST add a section starting with the exact tag `[TWIST]:` that reveals a final, shocking twist."

    return base_prompt + style_instruction


# 4. create a function to generate story from images
def generate_story_from_images(images_list, story_style:str, story_language:str)->str:
    """
    Generate a story from a list of images using a generative AI model.

    This function takes a sequence of images and a storytelling prompt,
    then sends them to the Gemini model to produce a narrative that 
    connects the images. The story will follow the specified style 
    (e.g., Morale, Mystery, Thriller) and will be written in the 
    specified target language.

    Args:
        images_list: A list of images (PIL images, base64, or model-supported
            image inputs) that will serve as the visual inspiration for the story.
        
        story_style (str): The genre/style of the story (e.g., "Morale",
            "Mystery", "Thriller").
        
        story_language (str): The language in which
            the story should be generated (e.g., "hindi", "english", tc).

    Returns:
        str: The text of the generated story produced by the model.
    """
     
    response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = [images_list, prompt(story_style, story_language)]
    )

    return response.text

# 5. create a wav function
def wave_file(pcm, channels=1, rate=24000, sample_width=2) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)
    buffer.seek(0)
    return buffer.read() 

# 6. create a function to generate audio of the story
def generate_audio(story:str, voice:str)->bytes:
    """
    Generate an audio narration of a story using a text-to-speech model.

    This function sends the input story text to the Gemini TTS model,
    configured with the specified voice. The model generates an audio
    version of the story in MP3 format and returns it as raw bytes.

    Args:
        story (str): The story text to be converted into speech.
        voice (str): The name of the prebuilt voice to use for narration.

    Returns:
        bytes: The generated audio data in MP3 format, represented as raw
        binary data. This can be saved to a file, streamed, or played 
        directly in applications like Streamlit using `st.audio`.
    """

    response = client.models.generate_content(
        model = "gemini-2.5-flash-preview-tts",
        contents= story,
        
        config= types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            
            speech_config=types.SpeechConfig(
                voice_config= types.VoiceConfig(
                    prebuilt_voice_config= types.PrebuiltVoiceConfig(
                        voice_name=voice
                    )
                )
            )
        )
    )

    data = response.candidates[0].content.parts[0].inline_data.data
    return wave_file(data)

   


