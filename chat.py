from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = input("Masukkan url toko : ")

if url:
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=selenium_profile")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(5)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#main > div > div.t5pFIU > div > div > div > div > div:nth-child(2) > div > div > div > div.stardust-tabs-panels > section:nth-child(1) > div > div.product-rating-overview > div.product-rating-overview__filters > div:nth-child(3)",
                )
            )
        )

        driver.find_element(
            By.CSS_SELECTOR,
            "#main > div > div.t5pFIU > div > div > div > div > div:nth-child(2) > div > div > div > div.stardust-tabs-panels > section:nth-child(1) > div > div.product-rating-overview > div.product-rating-overview__filters > div:nth-child(3)",
        ).click()

        print("Tombol ke-6 berhasil diklik")
        time.sleep(3)
    except Exception as e:
        print("Gagal klik tombol ke-6:", e)

    data = []

    for i in range(76):  # Loop 3 halaman
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.find_all("div", class_="shopee-product-rating__main")

        for container in containers:
            try:
                inner_divs = container.find_all("div", recursive=False)

                for div in inner_divs:
                    if not div.get("class"):  # div tanpa class
                        review = div.get_text(strip=True)
                        if review:
                            data.append(review)
                            break  # cukup satu review per container
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
            print("Gagal klik tombol berikutnya:", e)
            break

    print(data)
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("shopeeB4.csv", index=False)
    print("Berhasil disimpan ke shopee.csv")
