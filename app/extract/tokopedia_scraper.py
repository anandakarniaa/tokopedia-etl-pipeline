import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd

from app.config.settings import BASE_URL
from app.config.settings import SCROLL_COUNT
from app.utils.logger import logger


# =========================================================
# CREATE DRIVER
# =========================================================

def create_driver():
    """
    Create Chrome WebDriver.

    Supports:
    - Local Windows
    - Docker/Linux
    """

    options = Options()

    # =====================================================
    # COMMON OPTIONS
    # =====================================================

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_argument(
        "--disable-notifications"
    )

    options.add_argument(
        "--disable-popup-blocking"
    )

    options.add_argument(
        "--window-size=1920,1080"
    )

    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    # =====================================================
    # DOCKER / LINUX
    # =====================================================

    if os.path.exists("/usr/bin/chromium"):

        logger.info("Environment: Docker/Linux")

        options.binary_location = "/usr/bin/chromium"

        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(
            service=Service("/usr/bin/chromedriver"),
            options=options
        )

    # =====================================================
    # WINDOWS
    # =====================================================

    else:

        logger.info("Environment: Local Windows")

        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

    return driver


# =========================================================
# FIND PRODUCT NAME
# =========================================================

def find_product_name(card):
    """
    Try several selectors because Tokopedia CSS classes
    can change.
    """

    selectors = [

        # Current known selector
        (
            "span",
            {
                "class": "+tnoqZhn89+NHUA43BpiJg=="
            }
        ),

        # Generic product-name candidates
        (
            "div",
            {
                "data-testid": "linkProductName"
            }
        ),

        (
            "span",
            {
                "data-testid": "linkProductName"
            }
        ),

    ]

    for tag, attrs in selectors:

        element = card.find(tag, attrs)

        if element:

            text = element.get_text(
                strip=True
            )

            if text:
                return text

    return None


# =========================================================
# SCRAPE TOKOPEDIA
# =========================================================

def scrape_tokopedia():

    driver = create_driver()

    try:

        # =====================================================
        # 1. OPEN WEBSITE
        # =====================================================

        logger.info("=" * 60)
        logger.info("Membuka Tokopedia")
        logger.info("=" * 60)

        logger.info(
            f"URL: {BASE_URL}"
        )

        driver.get(BASE_URL)

        # =====================================================
        # 2. WAIT PAGE LOAD
        # =====================================================

        wait = WebDriverWait(
            driver,
            20
        )

        wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        logger.info(
            "Page load selesai"
        )

        time.sleep(5)

        # =====================================================
        # 3. DEBUG PAGE TITLE / URL
        # =====================================================

        logger.info(
            f"Current URL: {driver.current_url}"
        )

        logger.info(
            f"Page title: {driver.title}"
        )

        # =====================================================
        # 4. INFINITE SCROLL
        # =====================================================

        logger.info("=" * 60)
        logger.info("Mulai Infinite Scroll")
        logger.info("=" * 60)

        last_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        for i in range(SCROLL_COUNT):

            logger.info(
                f"Scroll ke-{i + 1}/{SCROLL_COUNT}"
            )

            driver.execute_script(
                "window.scrollTo("
                "0, document.body.scrollHeight"
                ");"
            )

            time.sleep(4)

            new_height = driver.execute_script(
                "return document.body.scrollHeight"
            )

            if new_height == last_height:

                logger.info(
                    "Sudah mencapai akhir halaman."
                )

                break

            last_height = new_height

        time.sleep(3)

        # =====================================================
        # 5. GET HTML
        # =====================================================

        html = driver.page_source

        # =====================================================
        # 6. SAVE DEBUG FILE
        # =====================================================

        try:

            with open(
                "debug_tokopedia.html",
                "w",
                encoding="utf-8"
            ) as f:

                f.write(html)

            driver.save_screenshot(
                "debug_tokopedia.png"
            )

            logger.info(
                "Debug HTML disimpan: "
                "debug_tokopedia.html"
            )

            logger.info(
                "Debug screenshot disimpan: "
                "debug_tokopedia.png"
            )

        except Exception as e:

            logger.warning(
                f"Gagal menyimpan debug file: {e}"
            )

        # =====================================================
        # 7. PARSE HTML
        # =====================================================

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # =====================================================
        # 8. FIND CARD
        # =====================================================

        all_cards = soup.find_all(
            "div",
            class_="css-5wh65g"
        )

        logger.info(
            f"Raw card ditemukan: {len(all_cards)}"
        )

        # =====================================================
        # 9. FALLBACK CARD DETECTION
        # =====================================================

        if not all_cards:

            logger.warning(
                "Selector css-5wh65g tidak menemukan card."
            )

            alternative_cards = soup.select(
                '[data-testid*="product"]'
            )

            if alternative_cards:

                logger.info(
                    "Fallback product container ditemukan: "
                    f"{len(alternative_cards)}"
                )

                all_cards = alternative_cards

        # =====================================================
        # 10. FILTER VALID PRODUCTS
        # =====================================================

        cards = []

        for card in all_cards:

            product_name = find_product_name(
                card
            )

            if product_name:

                cards.append(card)

        invalid_cards = (
            len(all_cards)
            - len(cards)
        )

        # =====================================================
        # 11. SCRAPING
        # =====================================================

        product_list = []
        price_list = []
        seller_list = []
        city_list = []
        sold_list = []
        rating_list = []

        for box in cards:

            # -------------------------------------------------
            # PRODUCT
            # -------------------------------------------------

            product = find_product_name(
                box
            )

            # -------------------------------------------------
            # PRICE
            # -------------------------------------------------

            price = None

            # Primary selector
            price_element = box.find(
                "div",
                class_="urMOIDHH7I0Iy1Dv2oFaNw=="
            )

            if price_element:

                price = price_element.get_text(
                    strip=True
                )

            # Fallback: search text containing "Rp"
            if not price:

                price_text = box.find(
                    string=lambda text:
                    text and "Rp" in text
                )

                if price_text:

                    price = price_text.strip()

            # Debug jika harga tidak ditemukan
            if not price:

                logger.warning(
                    f"Harga tidak ditemukan: {product}"
                )

            # -------------------------------------------------
            # SELLER
            # -------------------------------------------------

            seller_element = box.find(
                "span",
                class_=
                "si3CNdiG8AR0EaXvf6bFbQ== "
                "gxi+fsEljOjqhjSKqjE+sw== flip"
            )

            seller = (
                seller_element.get_text(
                    strip=True
                )
                if seller_element
                else None
            )

            # -------------------------------------------------
            # CITY
            # -------------------------------------------------

            lokasi = box.find_all(
                "span",
                class_=
                "gxi+fsEljOjqhjSKqjE+sw== flip"
            )

            city = (
                lokasi[-1].get_text(
                    strip=True
                )
                if lokasi
                else None
            )

            # -------------------------------------------------
            # SOLD
            # -------------------------------------------------

            sold_element = box.find(
                "span",
                class_="u6SfjDD2WiBlNW7zHmzRhQ=="
            )

            sold = (
                sold_element.get_text(
                    strip=True
                )
                if sold_element
                else None
            )

            # -------------------------------------------------
            # RATING
            # -------------------------------------------------

            rating_element = box.find(
                "span",
                class_="_2NfJxPu4JC-55aCJ8bEsyw=="
            )

            rating = (
                rating_element.get_text(
                    strip=True
                )
                if rating_element
                else None
            )

            # -------------------------------------------------
            # APPEND
            # -------------------------------------------------

            product_list.append(
                product
            )

            price_list.append(
                price
            )

            seller_list.append(
                seller
            )

            city_list.append(
                city
            )

            sold_list.append(
                sold
            )

            rating_list.append(
                rating
            )

        # =====================================================
        # 12. DATAFRAME
        # =====================================================

        df = pd.DataFrame({

            "Product Name": product_list,
            "Price": price_list,
            "Seller": seller_list,
            "City": city_list,
            "Sold": sold_list,
            "Rating": rating_list

        })

        # =====================================================
        # 13. DATA QUALITY
        # =====================================================

        if not df.empty:

            duplicate_count = (
                df["Product Name"]
                .duplicated()
                .sum()
            )

            unique_count = (
                df["Product Name"]
                .nunique()
            )

        else:

            duplicate_count = 0
            unique_count = 0

        # =====================================================
        # 14. SUMMARY
        # =====================================================

        print("=" * 60)

        print(
            "Jumlah card ditemukan      :",
            len(all_cards)
        )

        print(
            "Jumlah product valid       :",
            len(cards)
        )

        print(
            "Jumlah card tidak valid    :",
            invalid_cards
        )

        print(
            "Jumlah data hasil scraping :",
            len(df)
        )

        print(
            "Jumlah duplicate           :",
            duplicate_count
        )

        print(
            "Jumlah unique product      :",
            unique_count
        )

        print("=" * 60)

        # =====================================================
        # 15. FAIL FAST
        # =====================================================

        if df.empty:

            raise ValueError(
                "Scraping menghasilkan 0 data. "
                "File debug_tokopedia.html dan "
                "debug_tokopedia.png sudah dibuat. "
                "Periksa isi halaman yang diterima Docker."
            )

        return df

    finally:

        driver.quit()