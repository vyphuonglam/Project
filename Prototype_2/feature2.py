import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from openai import OpenAI
import fitz
import os
import folium
from streamlit_folium import st_folium
from gtts import gTTS


def app():
    st.title("WATER TESTING GUIDE")
    st.write("Welcome to WATER TESTING GUIDE")


    # Initialize the OpenAI client
    client = OpenAI(api_key="OPENAI_API_KEY")



    # ChatGPT help
    pdf_path = "PDF.pdf"
    def extract_text_from_pdf(pdf_path):    
        if not os.path.isfile(pdf_path):
            print("Error: File not found!")
        else:
            try:
                # Function to extract text from PDF
                def extract_text_from_pdf(pdf_path):
                    text = ""
                    with fitz.open(pdf_path) as pdf:
                        for page_num, page in enumerate(pdf, start=1):
                            text += f"--- Page {page_num} ---\n"
                            text += page.get_text()
                    return text
            except Exception as e:
                print(f"An error occurred: {e}")
    pdf_text = extract_text_from_pdf(pdf_path)
    def get_guided_instructions(pdf_content,prompt,model="gpt-3.5-turbo"):
        completion = client.chat.completions.create(
            model = model,
            messages = [{"role":"system", 
                        "content": "You are a water lines expert. Guide the user step-by-step how to check for leakage using this content: {pdf_content}. Feel free to replace any terms and make it easy to follow for students."},
                        {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

    # Title of the app
    st.title("DIY Water Quality Testing Guide")

    # Dropdown menu for selecting the test type
    test_options = [
        "Select a test",
        "House Line Test",
        "Pin Test",
        "Toilet Leak Test",
        "Flow Rate Measurement"
    ]
    selected_test = st.selectbox("Choose a water quality test to get started:", test_options)

    # Display information based on the selected test
    if selected_test == "House Line Test":
        st.subheader("House Line Test")
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform house line test that's easy to follow.", model="gpt-3.5-turbo")
        st.write(guided_instructions)
         # Text-to-speech conversion
        tts = gTTS(text=guided_instructions, lang='en')
        tts.save("guided_instructions.mp3")

        # Display audio player in Streamlit
        audio_file = open("guided_instructions.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    elif selected_test == "Pin Test":
        st.subheader("Pin Test")
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform the pin test that's easy to follow.",model="gpt-3.5-turbo")
        st.write(guided_instructions)
        # Text-to-speech conversion
        tts = gTTS(text=guided_instructions, lang='en')
        tts.save("guided_instructions.mp3")

        # Display audio player in Streamlit
        audio_file = open("guided_instructions.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    elif selected_test == "Toilet Leak Test":
        st.subheader("Toilet Leak Test")
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform the toilet leak test that's easy to follow.",model="gpt-3.5-turbo")
        st.write(guided_instructions)
        # Text-to-speech conversion
        tts = gTTS(text=guided_instructions, lang='en')
        tts.save("guided_instructions.mp3")

        # Display audio player in Streamlit
        audio_file = open("guided_instructions.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    elif selected_test == "Flow Rate Measurement":
        st.subheader("Flow Rate Measurement")
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform flow rate measurement that's easy to follow.",model="gpt-3.5-turbo")
        st.write(guided_instructions)
        # Text-to-speech conversion
        tts = gTTS(text=guided_instructions, lang='en')
        tts.save("guided_instructions.mp3")

        # Display audio player in Streamlit
        audio_file = open("guided_instructions.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    else:
        st.write("Please select a test to see the instructions.")