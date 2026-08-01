import requests
from bs4 import BeautifulSoup
import json
import os

USERNAME = "Nirlepb"

def fetch_data():
    url = f"https://github.com/users/{USERNAME}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    contributions = []
    days = soup.find_all("td", attrs={"data-date": True})
    
    for day in days:
        contributions.append({
            "date": day["data-date"],
            "level": int(day.get("data-level", 0))
        })

    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(contributions, f)
        
    print(f"Fetched {len(contributions)} days of contribution data for {USERNAME}.")

if __name__ == "__main__":
    fetch_data()