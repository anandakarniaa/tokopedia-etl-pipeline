from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

from app.config.settings import BASE_URL
from app.config.settings import SCROLL_COUNT


def scrape_tokopedia():

    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )
    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(BASE_URL)

    time.sleep(5)

    print("=" * 60)
    print("Mulai Infinite Scroll")
    print("=" * 60)

    last_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    for i in range(SCROLL_COUNT):

        print(f"Scroll ke-{i+1}")

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(3)

        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        if new_height == last_height:
            print("Sudah mencapai akhir halaman.")
            break

        last_height = new_height

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.find_all("div", class_="css-5wh65g")

    print("=" * 60)
    print("Jumlah Card :", len(cards))
    print("=" * 60)

    product_list = []
    price_list = []
    seller_list = []
    city_list = []
    sold_list = []
    rating_list = []

    for box in cards:

        # PRODUCT
        try:
            product = box.find(
                "span",
                class_="+tnoqZhn89+NHUA43BpiJg=="
            ).get_text(strip=True)
        except:
            product = None

        # PRICE
        try:
            price = box.find(
                "div",
                class_="urMOIDHH7I0Iy1Dv2oFaNw=="
            ).get_text(strip=True)
        except:
            price = None

        # SELLER
        try:
            seller = box.find(
                "span",
                class_="si3CNdiG8AR0EaXvf6bFbQ== gxi+fsEljOjqhjSKqjE+sw== flip"
            ).get_text(strip=True)
        except:
            seller = None

        # CITY
        try:
            lokasi = box.find_all(
                "span",
                class_="gxi+fsEljOjqhjSKqjE+sw== flip"
            )

            city = lokasi[-1].get_text(strip=True)

        except:
            city = None

        # SOLD
        try:
            sold = box.find(
                "span",
                class_="u6SfjDD2WiBlNW7zHmzRhQ=="
            ).get_text(strip=True)
        except:
            sold = None

        # RATING
        try:
            rating = box.find(
                "span",
                class_="_2NfJxPu4JC-55aCJ8bEsyw=="
            ).get_text(strip=True)
        except:
            rating = None

        product_list.append(product)
        price_list.append(price)
        seller_list.append(seller)
        city_list.append(city)
        sold_list.append(sold)
        rating_list.append(rating)

    driver.quit()

    df = pd.DataFrame({
        "Product Name": product_list,
        "Price": price_list,
        "Seller": seller_list,
        "City": city_list,
        "Sold": sold_list,
        "Rating": rating_list
    })

    print("=" * 60)
    print("Jumlah data :", len(df))
    print("=" * 60)

    return df