import io
import base64
import os
import streamlit as st
from openai import OpenAI

# Retrieve API key
API_KEY = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("🔑 OpenAI API key not found. Set STREAMLIT_SECRET or environment var OPENAI_API_KEY.")
    st.stop()
client = OpenAI(api_key=API_KEY)

# Encode image to base64 for GPT
def encode_image_base64(file):
    file.seek(0)
    data = file.read()
    b64 = base64.b64encode(data).decode()
    return f"data:image/jpeg;base64,{b64}"

# Send to GPT-4 Vision
def diagnose_skin_condition(img_b64):
    messages = [
        {"role":"system","content":(
            "You are a board-certified dermatologist AI assistant. "
            "A user has provided a clinical photograph. "
            "Provide the most likely diagnosis, confidence (0-100%), and reasoning."
        )},
        {"role":"user","content":[
            {"type":"text","text":"Analyze this clinical photo and diagnose the condition:"},
            {"type":"image_url","image_url":{"url":img_b64}}
        ]}
    ]
    resp = client.chat.completions.create(
        model="gpt-4o",  # update to your enabled image-capable model
        messages=messages,
        max_tokens=400,
        temperature=0
    )
    return resp.choices[0].message.content

# Streamlit UI setup
st.set_page_config(page_title="Skin Analyzer AI", layout="centered")
st.title("🧴 AI-Powered Skin Analyzer MVP")
st.markdown("Select or capture a clear skin photo and get an AI-driven diagnosis via GPT-4 Vision.")

# Let user choose between upload or camera capture
input_method = st.radio(
    label="How would you like to provide the skin image?",
    options=["Upload from device", "Capture via camera"]
)

if input_method == "Upload from device":
    uploaded = st.file_uploader(
        label="📸 Upload a skin image",
        type=["jpg", "jpeg", "png"]
    )
else:
    uploaded = st.camera_input(
        label="📷 Capture an image with your camera"
    )

if uploaded:
    st.image(uploaded, use_column_width=True, caption="Your selected image")
    confirm = st.checkbox("✅ Confirm this is the correct image to analyze")
    if confirm:
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
        st.info("Please confirm the image before proceeding with diagnosis.")
else:
    st.info("Please provide an image by uploading or capturing to begin.")
