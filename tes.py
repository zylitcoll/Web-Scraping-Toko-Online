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
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Klik checkbox ke-3 (index ke-2)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div#content-Rating label.checkbox")
            )
        )
        checkboxes = driver.find_elements(
            By.CSS_SELECTOR, "div#content-Rating label.checkbox"
        )

        if len(checkboxes) >= 5:
            checkboxes[1].click()  # checkbox ke-3
            checkboxes[2].click()  # checkbox ke-3
            checkboxes[3].click()  # checkbox ke-3
            checkboxes[4].click()  # checkbox ke-3

            print("Checkbox ke-3 diklik")
        else:
            print("Jumlah checkbox kurang dari 3")

        time.sleep(3)  # Tunggu halaman reload setelah klik filter

    except Exception as e:
        print("Gagal klik filter rating:", e)

    # SCRAPING DIMULAI
    data = []
    for i in range(0, 3):  # Loop 3 halaman
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll("article", attrs={"class": "css-1pr2lii"})

        for container in containers:
            try:
                review = container.find(
                    "span", attrs={"data-testid": "lblItemUlasan"}
                ).text
                data.append((review))
            except AttributeError:
                continue

        time.sleep(2)
        try:
            driver.find_element(
                By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']"
            ).click()
            time.sleep(3)
        except Exception as e:
            print("Tidak bisa klik laman berikutnya:", e)
            break

    print(data)
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("B4-B1.csv", index=False)
