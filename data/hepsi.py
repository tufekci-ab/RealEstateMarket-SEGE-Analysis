import csv
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Connect to Chrome Debugger
chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=chrome_options)

# Switch to the correct tab by URL
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "hepsiemlak.com" in driver.current_url:
        break
else:
    print("Hepsiemlak tab not found.")
    driver.quit()
    exit()

# Helper function to write rows
def write_rows(rows, csv_path: Path):
    mode = "a" if csv_path.exists() else "w"
    with csv_path.open(mode, newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if mode == "w":
            w.writerow([
                "ilan_id", "ilan_linki", "ilan_tarihi", "ilan_tipi",
                "metrekare", "bina_yasi", "kat", "konum",
                "fiyat", "para_birimi"
            ])
        for v in rows:
            w.writerow([
                v["id"], v["link"], v["tarih"], v["tip"],
                v["metrekare"], v["bina_yasi"], v["kat"], v["konum"],
                v["fiyat"], v["para_birimi"]
            ])

# Scrape all listings on the current page
def scrape_current_page():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.listingView"))
        )
    except TimeoutException:
        print("Listings did not load. If CAPTCHA exists, pass it and press Enter.")
        input()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.listingView"))
        )

    items = driver.find_elements(By.CSS_SELECTOR, "article.listingView")
    data = []
    for it in items:
        try:
            ilan_id = it.get_attribute("id")
            link = it.find_element(By.CSS_SELECTOR, "a.card-link").get_attribute("href")
            tarih = it.find_element(By.CSS_SELECTOR, "span.list-view-date").text.strip()
            tip = it.find_element(By.CSS_SELECTOR, "span.short-property > span.left").text.strip()
            metrekare = it.find_element(By.CSS_SELECTOR, "span.squareMeter").text.strip()
            bina_yasi = it.find_element(By.CSS_SELECTOR, "span.buildingAge").text.strip()
            kat = it.find_element(By.CSS_SELECTOR, "span.floortype").text.strip()
            konum = it.find_element(By.CSS_SELECTOR, "span.list-view-location").text.strip()

            price_text = it.find_element(By.CSS_SELECTOR, "span.list-view-price").text.strip()
            parts = price_text.split()
            fiyat = parts[0]
            para_birimi = parts[1] if len(parts) > 1 else ""

            data.append({
                "id": ilan_id,
                "link": link,
                "tarih": tarih,
                "tip": tip,
                "metrekare": metrekare,
                "bina_yasi": bina_yasi,
                "kat": kat,
                "konum": konum,
                "fiyat": fiyat,
                "para_birimi": para_birimi
            })
        except NoSuchElementException:
            continue

    print(f"{len(data)} listings scraped.")
    return data

# Loop through all pages
def scrape_all(csv_path: Path):
    total = 0
    while True:
        print(f"Page: {driver.current_url}")
        rows = scrape_current_page()
        write_rows(rows, csv_path)
        total += len(rows)

        try:
            nxt = driver.find_element(By.CSS_SELECTOR, "a.he-pagination__navigate-text--next")
            driver.execute_script("arguments[0].click();", nxt)
            time.sleep(1.0)
        except NoSuchElementException:
            print("No next page found. Scraping finished.")
            break

    print(f"Total {total} listings saved to {csv_path}")

# Main run
if __name__ == "__main__":
    out = Path("ilan_detaylari.csv")
    scrape_all(out)
    driver.quit()
