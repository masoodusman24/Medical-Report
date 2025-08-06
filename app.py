import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import openai
import os

# Load your OpenAI API key
openai.api_key = "your-openai-api-key"

st.title("🧾 Medical Report Assistant with Generative AI")

uploaded_file = st.file_uploader("Upload Medical Report (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])

def ocr_pdf(file):
    images = convert_from_path(file)
    text = ""
    for page in images:
        text += pytesseract.image_to_string(page)
    return text

def ocr_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

def ask_gpt(text):
    prompt = f"Please explain the following medical report in simple terms:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or gpt-4 if you have access
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if uploaded_file:
    with st.spinner("Extracting text from report..."):
        if uploaded_file.type == "application/pdf":
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())
            extracted_text = ocr_pdf("temp.pdf")
        else:
            extracted_text = ocr_image(uploaded_file)

    st.subheader("📄 Extracted Text")
    st.text_area("OCR Result", extracted_text, height=300)

    if st.button("🔍 Explain with AI"):
        with st.spinner("Asking AI to explain..."):
            explanation = ask_gpt(extracted_text)
            st.subheader("💡 AI Explanation")
            st.write(explanation)
