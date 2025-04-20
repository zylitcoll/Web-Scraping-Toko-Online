from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd

# Input URL toko
url = input("Masukkan url toko : ")

if url:
    options = uc.ChromeOptions()
    options.add_argument(
        "--user-data-dir=/home/why/.config/google-chrome/"
    )  # Profil kamu
    options.add_argument("--profile-directory=Profile 2")  # Ganti sesuai nama profilmu
    options.add_argument("--no-first-run")
    options.add_argument("--no-service-autorun")
    options.add_argument("--password-store=basic")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, headless=False)

    # 🧠 Tambahkan anti-bot JavaScript injection di awal dokumen
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )

    driver.get(url)
    time.sleep(random.uniform(3, 5))

    # Klik tab ulasan bintang 3
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#main > div > div.t5pFIU > div > div > div > div > div:nth-child(2) > div > div > div > div.stardust-tabs-panels > section:nth-child(1) > div > div.product-rating-overview > div.product-rating-overview__filters > div:nth-child(2)",
                )
            )
        ).click()
        print("Tombol filter bintang 3 berhasil diklik")
        time.sleep(random.uniform(2.5, 4))
    except Exception as e:
        print("Gagal klik tombol filter bintang 3:", e)

    # Scraping ulasan
    data = []
    for i in range(983):
        time.sleep(random.uniform(3, 5))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.find_all("div", class_="shopee-product-rating__main")

        for container in containers:
            try:
                inner_divs = container.find_all("div", recursive=False)
                for div in inner_divs:
                    if not div.get("class"):
                        review = div.get_text(strip=True)
                        if review:
                            data.append(review)
                            break
            except Exception as e:
                print("Gagal ambil review:", e)
                continue

        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "button.shopee-icon-button.shopee-icon-button--right",
                    )
                )
            )
            next_button.click()
        except Exception as e:
            print("Gagal klik tombol berikutnya (mungkin halaman terakhir):", e)
            break

    # Simpan hasil
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("shopee_bintang5.csv", index=False)
    print("Berhasil disimpan ke shopee_bintang3.csv")
