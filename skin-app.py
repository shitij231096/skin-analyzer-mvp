import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Skin Analyzer MVP", layout="centered")
st.title("🧴 Skin Analyzer (MVP)")
st.markdown("Upload or click a photo of your skin to begin analysis.")

# ✅ Dummy Diagnosis and Product Map
conditions = [
    {
        "name": "Acne Vulgaris",
        "advice": "Use a salicylic acid face wash and a non-comedogenic moisturizer.",
        "products": [
            {"name": "Neutrogena Oil-Free Acne Wash", "use": "Face wash", "link": "https://www.nykaa.com"},
            {"name": "The Ordinary Niacinamide 10%", "use": "Serum", "link": "https://www.nykaa.com"}
        ]
    },
    {
        "name": "Eczema",
        "advice": "Use a fragrance-free moisturizer with ceramides. Avoid hot water.",
        "products": [
            {"name": "CeraVe Moisturizing Cream", "use": "Moisturizer", "link": "https://www.nykaa.com"},
            {"name": "Aveeno Skin Relief Lotion", "use": "Body lotion", "link": "https://www.nykaa.com"}
        ]
    },
    {
        "name": "Seborrheic Dermatitis",
        "advice": "Use a gentle anti-fungal shampoo on affected areas. Moisturize regularly.",
        "products": [
            {"name": "Nizoral Anti-Dandruff Shampoo", "use": "Shampoo", "link": "https://www.nykaa.com"},
            {"name": "Bioderma Sensibio DS+ Cream", "use": "Face cream", "link": "https://www.nykaa.com"}
        ]
    },
    {
        "name": "Rosacea",
        "advice": "Avoid spicy food and heat. Use a soothing, alcohol-free toner.",
        "products": [
            {"name": "La Roche-Posay Toleriane Toner", "use": "Toner", "link": "https://www.nykaa.com"},
            {"name": "Avene Antirougeurs Fort Cream", "use": "Redness reducer", "link": "https://www.nykaa.com"}
        ]
    }
]

image_file = st.file_uploader("Upload a skin image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Your uploaded image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    if st.button("Submit for Analysis"):
        st.info("🔍 Analyzing image...")

        condition = random.choice(conditions)
        st.markdown(f"### 🧠 **Likely condition:** _{condition['name']}_")
        st.markdown(f"💡 **Suggested care:** {condition['advice']}")

        st.markdown("### 🛒 Recommended Products:")
        for product in condition['products']:
            st.markdown(f"- **{product['name']}** ({product['use']}) — [Buy]({product['link']})")
else:
    st.info("Please upload or take a photo to continue.")

st.markdown("---")
st.caption("This is a prototype. Diagnosis is simulated. No data is stored.")
