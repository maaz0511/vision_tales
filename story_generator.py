from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import wave
from gtts import gTTS
from io import BytesIO
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

# 5. create a function to generate audio of the story
def generate_audio(story: str) -> BytesIO:
    """
    Generate speech audio from text using gTTS.
    Detects the story's language via Gemini and returns the audio as an in-memory MP3 buffer.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"Return ONLY the ISO 639-1 language code (like 'en', 'fr', 'es') for this text: {story}"
    )

    # Extract language code safely
    lang_code = response.candidates[0].content.parts[0].text.strip().lower()

    # Sanitize possible extra characters (e.g., quotes)
    lang_code = lang_code.replace("'", "").replace('"', '')

    try:
        tts = gTTS(text=story, lang="en", slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp  # return BytesIO for streaming
    except Exception as e:
        raise RuntimeError(f"gTTS failed with language='{lang_code}': {e}")
