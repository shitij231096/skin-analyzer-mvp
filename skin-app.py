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
