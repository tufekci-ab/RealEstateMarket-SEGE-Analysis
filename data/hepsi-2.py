import csv
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

target_file = "extra-data-targets.csv"
output_file = f"extra-data.csv"


df = pd.read_csv(target_file)
if "ilan_id" not in df.columns:
    raise ValueError("The CSV must contain a column named 'ilan_id'.")

ilan_ids = df["ilan_id"].dropna().astype(str).tolist()


chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)

#field mapping
label_map = {
    "İlan no": "ilan_id",
    "Oda Sayısı": "oda_sayisi",
    "Banyo Sayısı": "banyo_sayisi",
    "Kat Sayısı": "kat_sayisi",
    "Isınma Tipi": "isinma_tipi",
    "Cephe": "cephe",
    "Kullanım Durumu": "kullanim_durumu"
}
fieldnames = list(label_map.values())


with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()


processed_ids = set()

#scraping
for ilan_id in ilan_ids:
    if ilan_id in processed_ids:
        print(f"[!] {ilan_id} already processed, skipping.")
        continue

    try:
        search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Konum']")
        search_box.clear()
        search_box.send_keys(ilan_id)

        previous_url = driver.current_url.strip()
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)
        current_url = driver.current_url.strip()

        if current_url == previous_url:
            print(f"[×] {ilan_id} → Page did not change. Listing may not exist.")
            row = {field: "NA" for field in fieldnames}
            row["ilan_id"] = ilan_id
            with open(output_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(row)
            continue

        row = {field: "" for field in fieldnames}
        specs = driver.find_elements(By.CSS_SELECTOR, "li.spec-item")
        for spec in specs:
            try:
                label = spec.find_element(By.CSS_SELECTOR, "span").text.strip()
                if label in label_map:
                    value = spec.find_element(By.CSS_SELECTOR, "span.value-txt").text.strip()
                    row[label_map[label]] = value
            except:
                continue

        row["ilan_id"] = ilan_id
        processed_ids.add(ilan_id)
        print(f"[✓] {ilan_id} -> OK")

        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)

    except Exception as err:
        print(f"[!] {ilan_id} -> ERROR: {err}")

print(f"\nAll listings processed: {output_file}")
driver.quit()
