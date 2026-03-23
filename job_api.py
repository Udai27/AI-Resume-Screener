from pathlib import Path
from dotenv import load_dotenv
import os
import requests

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

print("APP_ID:", os.getenv("ADZUNA_APP_ID"))
APP_ID = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")

def fetch_job_description(role):
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": API_KEY,
        "what": role,
        "results_per_page": 5,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        descriptions = []

        for job in data.get("results", []):
            descriptions.append(job.get("description", ""))

        return " ".join(descriptions)
    else:
        return ""
