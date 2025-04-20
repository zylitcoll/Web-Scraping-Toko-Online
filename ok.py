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
    time.sleep(3)

    data = []
    for i in range(0, 7):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll("div", attrs={"class": "shopee-product-rating__main"})

        for container in containers:
            try:
                review = container.find(
                    "div",
                    attrs={
                        "style": "position: relative; box-sizing: border-box; margin: 15px 0px; font-size: 14px; line-height: 20px; color: rgba(0, 0, 0, 0.87); word-break: break-word; white-space: pre-wrap;"
                    },
                ).text
                data.append((review))
            except AttributeError:
                continue

        time.sleep(2)
        driver.find_element(
            By.CSS_SELECTOR,
            "button.shopee-icon-button shopee-icon-button--right",
        ).click()
        time.sleep(3)

    print(data)
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("shopee.csv", index=False)
