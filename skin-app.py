from PIL import Image
import base64
import io
import openai
import os
import json
import streamlit as st

openai.api_key = st.secrets["openai_api_key"]

def encode_image(uploaded_file):
    image_copy = io.BytesIO(uploaded_file.getvalue())
    image_bytes = image_copy.read()
    b64 = base64.b64encode(image_bytes).decode()
    return f"data:image/jpeg;base64,{b64}"

def match_skin_condition(user_image, derm_data):
    encoded_img = encode_image(user_image)

    sample_conditions = list(derm_data.items())[:5]
    condition_texts = ""
    for name, entry in sample_conditions:
        condition_texts += f"\n### Condition: {name}\nImage: {entry['image_url']}\nDescription: {entry['description']}\n"

    prompt = f"""
You are a dermatologist AI assistant. A user has uploaded a photo of a skin condition.

Below are 5 known skin conditions with example images and medical descriptions (from DermNet).

Your job is to:
1. Compare the user's image with the samples.
2. Identify the **most likely match**.
3. Briefly explain why.

User Image: (shown below)

{condition_texts}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a medical assistant that diagnoses common skin conditions based on image matching."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": encoded_img}}
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

@st.cache_data(show_spinner=True)
def scrape_dermnet():
    base_url = "https://dermnetnz.org"
    image_index_url = f"{base_url}/images"

    try:
        response = requests.get(image_index_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all condition cards
        cards = soup.select("a.block")

        scraped_data = {}

        for card in cards[:15]:  # Limit to 15 conditions for speed
            try:
                title = card.select_one("h3").text.strip()
                image_url = card.select_one("img")["src"]
                if image_url.startswith("/"):
                    image_url = base_url + image_url

                page_url = base_url + card["href"]

                # Go to the page to get description
                condition_page = requests.get(page_url)
                cond_soup = BeautifulSoup(condition_page.text, 'html.parser')
                desc_tag = cond_soup.find("p")
                description = desc_tag.get_text().strip() if desc_tag else "No description found."

                scraped_data[title] = {
                    "image_url": image_url,
                    "description": description,
                    "page": page_url
                }

            except Exception as e:
                scraped_data[card["href"]] = {"error": str(e)}

        # Save to JSON
        with open("dermnet_conditions.json", "w") as f:
            json.dump(scraped_data, f, indent=2)

        return scraped_data

    except Exception as e:
        return {"error": str(e)}

st.set_page_config(page_title="Skin Analyzer AI", layout="centered")
st.title("🧴 AI-Powered Skin Analyzer")
st.markdown("Upload a photo of your skin and get a likely diagnosis based on DermNet samples using GPT-4 Vision.")

# ✅ Upload image section
image_file = st.file_uploader("📸 Upload or capture a skin image", type=["jpg", "jpeg", "png"])

if image_file:
    st.image(image_file, caption="Your uploaded image", use_column_width=True)

    # ✅ Load or scrape DermNet data
    if not os.path.exists("dermnet_conditions.json"):
        st.warning("🛠️ No existing condition database found. Scraping DermNet now...")
        derm_data = scrape_dermnet()
        st.markdown("### 🗂️ Sample Reference Conditions Used:")
        for name, entry in list(derm_data.items())[:5]:
            with st.expander(f"{name}"):
                if "image_url" in entry and entry["image_url"]:
                    st.image(entry["image_url"], width=300)
                else:
                    st.warning("⚠️ No image available for this condition.")
        
                st.write(entry.get("description", "No description available."))

    else:
        with open("dermnet_conditions.json", "r") as f:
            derm_data = json.load(f)

    # ✅ Button to call GPT-4 Vision
    if st.button("🔍 Submit for AI Diagnosis"):
        st.info("Analyzing your image using GPT-4 Vision...")
        try:
            result = match_skin_condition(image_file, derm_data)
            st.success("✅ Diagnosis complete!")
            st.markdown("### 🧠 AI Diagnosis Result:")
            st.markdown(result, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ GPT-4 Vision failed: {e}")
else:
    st.info("Please upload or capture a skin image to begin.")
