import urllib.request
import urllib.parse
import json
from html.parser import HTMLParser
import csv
import re
import time

# ---------------------------
# Configuration
# ---------------------------
API_URL = "https://www.volunteerconnector.org/api/search/"
API_HEADERS = {
    "User-Agent": "Mozilla/5.0"
    # "Authorization": "Bearer YOUR_API_KEY_HERE"  # uncomment if needed
}
API_PARAMS = {
    # "city": "San Jose",
    # "state": "CA",
    # "cause": "education",
    "limit": 50
}


# ---------------------------
# HTML Parser
# ---------------------------
class OpportunityParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_p = False
        self.in_category = False
        self.title = ""
        self.description = ""
        self.category = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.in_title = True
        elif tag == "p":
            self.in_p = True
        elif tag == "span" and attrs.get("class") == "category":
            self.in_category = True

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_title = False
        elif tag == "p":
            self.in_p = False
        elif tag == "span":
            self.in_category = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip() + " "
        elif self.in_p:
            self.description += data.strip() + " "
        elif self.in_category:
            self.category += data.strip() + " "


# ---------------------------
# Fetch URLs from API
# ---------------------------
def fetch_api_urls(api_url, params, headers):
    query_string = urllib.parse.urlencode(params)
    url = api_url + "?" + query_string
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read().decode("utf-8")
            json_data = json.loads(data)
    except Exception as e:
        print("Error fetching API data:", e)
        return []

    # Recursively find all URLs in JSON
    def find_urls(obj):
        urls = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                urls.extend(find_urls(v))
        elif isinstance(obj, list):
            for item in obj:
                urls.extend(find_urls(item))
        elif isinstance(obj, str):
            if re.match(r'^https?://', obj):
                urls.append(obj)
        return urls

    all_urls = find_urls(json_data)
    return list(set(all_urls))  # remove duplicates


# ---------------------------
# Parse individual opportunity
# ---------------------------
def parse_opportunity(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")

        parser = OpportunityParser()
        parser.feed(html)

        title = parser.title.strip() or "No Title"
        description = parser.description.strip() or "No Description"
        category = parser.category.strip()

        # Keyword-based category fallback
        if not category:
            text = (title + " " + description).lower()
            if "education" in text:
                category = "Education"
            elif "health" in text:
                category = "Health"
            elif "environment" in text:
                category = "Environment"
            elif "animal" in text:
                category = "Animals"
            else:
                category = "Other"

        return {"title": title, "description": description, "category": category, "url": url}

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


# ---------------------------
# Main workflow
# ---------------------------
def main():
    print("Fetching URLs from API...")
    urls = fetch_api_urls(API_URL, API_PARAMS, API_HEADERS)
    print(f"Found {len(urls)} URLs.")

    opportunities = []

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Parsing {url}")
        opp = parse_opportunity(url)
        if opp:
            opportunities.append(opp)
        time.sleep(1)  # polite delay

    # Sort by category
    opportunities.sort(key=lambda x: x["category"])

    # Save to CSV
    csv_file = "volunteer_opportunities.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "description", "category", "url"])
        writer.writeheader()
        for opp in opportunities:
            writer.writerow(opp)

    print(f"Done! {len(opportunities)} opportunities saved to {csv_file}")


if __name__ == "__main__":
    main()
