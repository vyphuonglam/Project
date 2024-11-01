
import streamlit as st
from openai import OpenAI
import fitz
import os

# Initialize OpenAI client
client = OpenAI(api_key="OPENAI_API_KEY")

###Feature 1
""""
# Function to get AI-generated text for water testing guides, tips, and FAQs
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a water testing expert with a background in environmental science, focused on providing simple guides, tips, and FAQs for DIY water testing. Provide a clear, concise response of up to three paragraphs, using bullet points for clarity. Use verbs like guide, explain, clarify, recommend, and identify to keep instructions actionable and easy to follow. This is a DIY water testing guide for residents. The goal is to help readers understand the importance of testing, recognize common contaminants, and interpret results without professional assistance. Use a friendly, informative, and approachable tone, suitable for homeowners and families. Avoid technical jargon. Exclude overly technical terms, complex chemical names, and steps requiring lab equipment or professional tools."},
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content


st.title("Water Testing Information Hub")
st.write("Learn about water testing basics, including why it's essential, which contaminants to check for, and how to interpret results.")

with st.form(key="water_testing_chat"):
    prompt = st.text_input("Enter your question or topic (e.g., 'Why is water testing important?', 'What contaminants should I test for?')")

    submitted = st.form_submit_button("Submit")

    if submitted:
        response = get_completion(prompt)
        st.write(response)

"""



###Feature 2: Guide to water test
#The provided guide

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
elif selected_test == "Pin Test":
    st.subheader("Pin Test")
    guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform the pin test that's easy to follow.",model="gpt-3.5-turbo")
    st.write(guided_instructions)
elif selected_test == "Toilet Leak Test":
    st.subheader("Toilet Leak Test")
    guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform the toilet leak test that's easy to follow.",model="gpt-3.5-turbo")
    st.write(guided_instructions)
elif selected_test == "Flow Rate Measurement":
    st.subheader("Flow Rate Measurement")
    guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform flow rate measurement that's easy to follow.",model="gpt-3.5-turbo")
    st.write(guided_instructions)
else:
    st.write("Please select a test to see the instructions.")









###Feature 3