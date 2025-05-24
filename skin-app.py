import io
import base64
import openai
import streamlit as st

# Load your API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

# Function to encode uploaded image to base64
def encode_image_to_base64(uploaded_file):
    image_bytes = uploaded_file.read()
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:image/jpeg;base64,{b64}"

# Function to send image directly to GPT-4 Vision for diagnosis
def diagnose_skin_condition(image_base64):
    messages = [
        {"role": "system", "content": (
            "You are a board-certified dermatologist AI assistant. "
            "A user has uploaded a clinical photo of a skin condition. "
            "Examine the image and provide the most likely diagnosis, "
            "confidence level (0-100%), and a brief explanation of your reasoning."
        )},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please analyze the following clinical photograph and diagnose the condition:"},
                {"type": "image_url", "image_url": {"url": image_base64}}
            ]
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=400,
        temperature=0.0
    )
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="Skin Analyzer AI", layout="centered")
st.title("🧴 AI-Powered Skin Analyzer MVP")
st.markdown(
    "Upload a clear photo of the skin concern and get an instant AI-driven diagnosis powered by GPT-4 Vision."
)

uploaded_file = st.file_uploader(
    label="📸 Upload or capture a skin image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    # Show preview
    st.image(uploaded_file, caption="Your uploaded image", use_column_width=True)

    if st.button("🔍 Diagnose with AI"):
        st.info("Analyzing… please wait.")
        try:
            # Reset file pointer and encode image
            uploaded_file.seek(0)
            img_b64 = encode_image_to_base64(uploaded_file)

            # Call GPT-4 Vision
            diagnosis = diagnose_skin_condition(img_b64)

            st.success("✅ Diagnosis complete!")
            st.markdown("### 🧠 AI Diagnosis Result:")
            st.markdown(diagnosis)
        except Exception as e:
            st.error(f"❌ Analysis error: {e}")
else:
    st.info("Please upload an image of the skin condition to begin.")
