import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os

st.set_page_config(page_title="Skin Analyzer MVP", layout="centered")
st.title("🧴 Skin Analyzer (MVP)")
st.markdown("We'll now scrape DermNet for common skin conditions...")

# ✅ Step 1: Scrape data only if not already saved
@st.cache_data(show_spinner=True)
def scrape_dermnet():
    base_url = "https://dermnetnz.org"
    image_library_url = "https://dermnetnz.org/image-library"

    try:
        response = requests.get(image_library_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        condition_links = soup.select("a.css-1bp1ao4")  # A-Z condition links
        condition_urls = [base_url + link['href'] for link in condition_links if link['href'].startswith("/topics")]

        scraped_data = {}

        for url in condition_urls[:10]:  # limit to 10 for now
            try:
                page = requests.get(url)
                page_soup = BeautifulSoup(page.text, 'html.parser')

                title = page_soup.find("h1").get_text().strip()
                desc_tag = page_soup.find("p")
                description = desc_tag.get_text().strip() if desc_tag else "No description available."

                img_tag = page_soup.find("img")
                image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

                scraped_data[title] = {
                    "description": description,
                    "image_url": image_url,
                    "page": url
                }

            except Exception as e:
                scraped_data[url] = {"error": str(e)}

        # Save to JSON
        with open("dermnet_conditions.json", "w") as f:
            json.dump(scraped_data, f, indent=2)

        return scraped_data

    except Exception as e:
        return {"error": str(e)}

# ✅ Run scraper and display data
if not os.path.exists("dermnet_conditions.json"):
    st.info("Scraping conditions from DermNet...")
    result = scrape_dermnet()
    if "error" in result:
        st.error(f"Scraping failed: {result['error']}")
    else:
        st.success("Scraping complete! Showing 10 conditions:")
        for title, entry in result.items():
            st.markdown(f"### 🧾 {title}")
            st.image(entry["image_url"], width=300)
            st.markdown(f"**Description**: {entry['description']}")
else:
    st.success("✅ dermnet_conditions.json already exists. Ready for GPT-4 matching.")
    with open("dermnet_conditions.json", "r") as f:
        data = json.load(f)
        for title, entry in data.items():
            st.markdown(f"### 🧾 {title}")
            st.image(entry["image_url"], width=300)
            st.markdown(f"**Description**: {entry['description']}")
