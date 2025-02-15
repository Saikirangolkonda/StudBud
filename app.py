import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF for PDF extraction

# Configure API Key
API_KEY = "AIzaSyDvPXNjxYSQcRP7rOIY3VlF8MzKlwHdgvo"
genai.configure(api_key=API_KEY)

# Initialize models for different tasks
study_plan_model = genai.GenerativeModel(model_name="gemini-pro")  # Study plan generation
material_analysis_model = genai.GenerativeModel(model_name="gemini-pro-vision")  # Material processing

# Streamlit UI
st.set_page_config(page_title="📚 Studbud: AI Personalized Study Planner", layout="centered")
st.title("📚 Studbud: AI Personalized Study Planner")
st.write("Get a customized study plan based on your study topics or uploaded materials.")

# User input
user_input = st.text_area("✏️ Enter your study topic or question:")

# 📌 Customization Options
st.subheader("🎯 Customize Your Study Plan")
duration = st.selectbox("📅 Study Duration", ["1 Week", "1 Month", "3 Months"])
pace = st.selectbox("🚀 Learning Pace", ["Slow", "Medium", "Fast"])
style = st.selectbox("🎓 Preferred Study Style", ["Text-based", "Video-based", "Practice-heavy"])

# File upload option
uploaded_file = st.file_uploader("📂 Upload a study material (PDF)", type=["pdf"])
extracted_text = ""

if uploaded_file:
    st.info("📄 Extracting text from uploaded PDF...")
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    extracted_text = "\n".join([page.get_text() for page in doc])
    st.text_area("📜 Extracted Text", extracted_text, height=200)

# Generate study plan button
if st.button("🎯 Generate Study Plan"):
    if user_input.strip():
        with st.spinner("📝 Creating your personalized study plan..."):
            prompt = f"Create a {duration} study plan with a {pace} learning pace focusing on {style} learning. Topic: {user_input}"
            response = study_plan_model.generate_content(prompt)
            st.subheader("📖 Your Personalized Study Plan:")
            st.write(response.text)
    else:
        st.warning("⚠️ Please enter a study topic.")

# Analyze uploaded material button
if uploaded_file and st.button("📘 Analyze Uploaded Study Material"):
    with st.spinner("🔍 Analyzing your study material..."):
        response = material_analysis_model.generate_content(extracted_text)
        st.subheader("📚 Insights from Uploaded Material:")
        st.write(response.text)
