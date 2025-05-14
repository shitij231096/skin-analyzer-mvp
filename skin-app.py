import streamlit as st
from PIL import Image

# ✅ Page setup
st.set_page_config(page_title="Skin Analyzer MVP", layout="centered")
st.title("🧴 Skin Analyzer (MVP)")
st.markdown("Upload or click a photo of your skin to begin analysis.")

# ✅ Upload image
image_file = st.file_uploader("Upload a skin image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if image_file:
    image = Image.open(image_file)
    st.image(image, caption="Your uploaded image", use_column_width=True)
    st.success("✅ Image uploaded successfully!")

    # ✅ Placeholder logic for now
    if st.button("Submit for Analysis"):
        st.info("🔍 Analyzing image...")
        st.markdown("### 🧠 **Likely condition:** _Acne Vulgaris_")
        st.markdown("💡 Suggested treatment: Use a face wash with salicylic acid twice a day.")
else:
    st.info("Please upload or take a photo to continue.")

# ✅ Footer
st.markdown("---")
st.caption("This is a prototype. No data is stored.")
