import streamlit as st
from PIL import Image
import random

# ✅ Page setup
st.set_page_config(page_title="Skin Analyzer MVP", layout="centered")
st.title("🧴 Skin Analyzer (MVP)")
st.markdown("Upload or click a photo of your skin to begin analysis.")

# ✅ Image Upload
image_file = st.file_uploader("Upload a skin image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

# ✅ Dummy Diagnosis Options
dummy_conditions = [
    {
        "name": "Acne Vulgaris",
        "advice": "Use a salicylic acid face wash and a non-comedogenic moisturizer."
    },
    {
        "name": "Eczema",
        "advice": "Use a fragrance-free moisturizer with ceramides. Avoid hot water."
    },
    {
        "name": "Seborrheic Dermatitis",
        "advice": "Use a gentle anti-fungal shampoo on affected areas. Moisturize regularly."
    },
    {
        "name": "Rosacea",
        "advice": "Avoid spicy food and heat. Use a soothing, alcohol-free toner."
    }
]

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Your uploaded image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    if st.button("Submit for Analysis"):
        st.info("🔍 Analyzing image...")

        # 🧠 Dummy condition generator
        condition = random.choice(dummy_conditions)
        st.markdown(f"### 🧠 **Likely condition:** _{condition['name']}_")
        st.markdown(f"💡 **Suggested care:** {condition['advice']}")
else:
    st.info("Please upload or take a photo to continue.")

# ✅ Footer
st.markdown("---")
st.caption("This is a prototype. Diagnosis is simulated. No data is stored.")
