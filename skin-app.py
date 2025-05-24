import io
import base64
import os
import streamlit as st
from openai import OpenAI

# Retrieve API key: prefer STREAMLIT secrets, fallback to environment variable
API_KEY = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("🔑 OpenAI API key not found. Set STREAMLIT_SECRET or environment var OPENAI_API_KEY.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

# Encode uploaded image to base64
def encode_image_base64(file):
    file.seek(0)
    data = file.read()
    b64 = base64.b64encode(data).decode()
    return f"data:image/jpeg;base64,{b64}"

# Send image to GPT-4 Vision
def diagnose_skin_condition(img_b64):
    messages = [
        {"role": "system", "content": (
            "You are a board-certified dermatologist AI assistant. "
            "A user has uploaded a clinical photograph of a skin condition. "
            "Provide the most likely diagnosis, confidence (0-100%), and reasoning."
        )},
        {"role": "user", "content": [
            {"type": "text", "text": "Analyze this clinical photo and diagnose the condition:"},
            {"type": "image_url", "image_url": {"url": img_b64}}
        ]}
    ]
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=400,
        temperature=0
    )
    return resp.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="Skin Analyzer AI", layout="centered")
st.title("🧴 AI-Powered Skin Analyzer MVP")
st.markdown("Upload a clear skin photo and get an AI-driven diagnosis via GPT-4 Vision.")

uploaded = st.file_uploader("📸 Upload a skin image", type=["jpg","jpeg","png"])
if uploaded:
    st.image(uploaded, use_column_width=True)
    if st.button("🔍 Diagnose with AI"):
        st.info("Analyzing... please wait.")
        try:
            img_b64 = encode_image_base64(uploaded)
            result = diagnose_skin_condition(img_b64)
            st.success("✅ Diagnosis complete!")
            st.markdown("### 🧠 Diagnosis Result:")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ Analysis error: {e}")
else:
    st.info("Please upload an image to begin.")
