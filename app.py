import streamlit as st
from PIL import Image
from story_generator import generate_audio, generate_story_from_images

st.markdown("<h1 style='text-align: center;'>VisionTales</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'><i>Where your pictures come alive as stories.</h2>", unsafe_allow_html=True)
st.markdown("Upload 1 to 10 images,choose an style and let AI write and narrate an story for you.")

with st.sidebar:
    st.header("Controls")

    # 1. upload images
    uploaded_images = st.file_uploader(
        "Upload Images", 
        type=["png", "jpeg", "jpg"], 
        accept_multiple_files=True)
    
    st.markdown("Upload maximum of 10 images.")


    # 2. select story styles
    story_style = st.selectbox(
        "Choose any style",
        ("Comedy", "Thriller", "Fairy Tale", "Sci-Fi", "Mystery", "Adventure", "Morale")
    )

    # 3. select language
    language = st.text_input("Language")

    # 4. button to generate the story
    generate_button = st.button("Generate Story", type='primary')


# main logic

if generate_button:
    
    if not uploaded_images:
        st.warning("Please upload atleast 1 image.")
    
    elif len(uploaded_images) > 10:
        st.warning("Please upload maximum of 10 images.")

    else:
        with st.spinner("The AI is writing and narrating your story..... This may take few moments."):
            
            images_list = [Image.open(image) for image in uploaded_images]

            st.write("Your Images")
            columns = st.columns(len(images_list))

            for index, image in enumerate(images_list):
                # we extract index and that index image from list of images.
                with columns[index]:
                    st.image(image, use_container_width=True)

            story = generate_story_from_images(images_list, story_style, language)
            
            st.subheader("Your Story:")
            if "Error" in story or "failed" in story or "API KEY" in story:
                st.error(story)
            
            else:
                st.success(story)


            st.subheader("Listen to your Story:")

            audio = generate_audio(story)
            st.audio(audio, format='audio/mp3')

