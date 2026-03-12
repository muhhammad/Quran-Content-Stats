import requests
import json

url = "https://api.alquran.cloud/v1/quran/quran-uthmani"

response = requests.get(url)
data = response.json()

quran = {}

for surah in data["data"]["surahs"]:
    surah_number = surah["number"]
    ayahs = []

    for ayah in surah["ayahs"]:
        ayahs.append(ayah["text"])

    quran[surah_number] = ayahs

with open("quran.json", "w", encoding="utf-8") as f:
    json.dump(quran, f, ensure_ascii=False, indent=2)

print("Quran JSON file created successfully.")