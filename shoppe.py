from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Ganti dengan URL halaman Shopee yang ingin kamu scraping
url = input("Masukkan URL produk Shopee: ")
driver.get(url)

# Tunggu konten terbuka penuh
time.sleep(5)

# Klik tombol ke-6 di bagian pagination review
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#main > div > div.t5pFIU > div > div > div > div > div:nth-child(2) > div > div > div > div.stardust-tabs-panels > section:nth-child(1) > div > div.product-ratings__list > nav > button:nth-child(6)",
            )
        )
    )

    driver.find_element(
        By.CSS_SELECTOR,
        "#main > div > div.t5pFIU > div > div > div > div > div:nth-child(2) > div > div > div > div.stardust-tabs-panels > section:nth-child(1) > div > div.product-ratings__list > nav > button:nth-child(6)",
    ).click()

    print("Tombol ke-6 berhasil diklik")
    time.sleep(3)
except Exception as e:
    print("Gagal klik tombol ke-6:", e)

# Ambil page source dan parsing dengan BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Ambil semua ulasan
all_reviews = soup.select("div.shopee-product-rating__main")

# Cek apakah minimal ada 5 ulasan
if len(all_reviews) >= 5:
    try:
        target_div = all_reviews[4].find_all("div")[3]  # Ulasan ke-5, div ke-4
        print("Isi teks ulasan ke-5:")
        print(target_div.get_text(strip=True))
    except Exception as e:
        print("Gagal mengambil teks ulasan ke-5:", e)
else:
    print("Jumlah ulasan tidak cukup untuk mengambil yang ke-5.")

# Tutup browser
driver.quit()
