from datetime import datetime
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver import Keys

from scarping_learning.connect_mongo import get_connection
from scarping_learning.models import City, Notice

db = get_connection()
if db is None:
    raise Exception("no connection to mongo db!")


def get_page_soup(geo_id: int, section_id: int, page: int = 1) -> BeautifulSoup:
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    url = f"https://market.lun.ua/uk/search?currency=USD&geo_id={geo_id}&is_without_fee=false&page={page}&price_sqm_currency=USD&section_id={section_id}&sort=insert_time&without_broker=owner"

    driver.get(url)
    time.sleep(2)

    driver.find_element(by=By.XPATH, value='//button[normalize-space()="$"]').click()
    time.sleep(2)

    page_height = driver.execute_script("return document.body.scrollHeight;")
    window_height = driver.find_element(by=By.TAG_NAME, value='body').size["height"]

    total_height = 0
    while total_height <= page_height:
        driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        total_height += window_height

    src = driver.page_source
    driver.quit()

    return BeautifulSoup(src, "lxml")


def fill_all_cities(soup: BeautifulSoup) -> None:
    cities_list = soup.find_all("a", class_="NavigationCitySelect-item")

    for link in cities_list:
        url_local = link.get("href")
        if url_local.find("geo_id") == -1:
            continue

        city_id = url_local[url_local.find("=") + 1: url_local.find("&")]
        city_name = link.find_next("span").text
        print(f"{city_name} {city_id}")

        City.objects(city_id=city_id).update_one(city_name=city_name,
                                                 city_id=city_id,
                                                 upsert=True)

    last_cities = [{"city_id": "1", "city_name": "Київ"},
                   {"city_id": "24", "city_name": "Львів"},
                   {"city_id": "26", "city_name": "Одеса"},
                   {"city_id": "16", "city_name": "Дніпро"},
                   {"city_id": "31", "city_name": "Харків"}]

    for obj in last_cities:
        City.objects(city_id=obj["city_id"]).update_one(city_name=obj["city_name"],
                                                        city_id=obj["city_id"],
                                                        upsert=True)


def handle_notices(soup: BeautifulSoup, city_id: int) -> None:
    list_of_articles = soup.find_all("article")
    for article in list_of_articles:

        article_id = article.get("id")

        picture_preview = article.find_next("picture", class_="realty-preview__image")
        if not picture_preview:
            continue
        picture = picture_preview.find_next("img").get("src")

        description = article.find_next(class_="realty-preview__content-column")
        if not description:
            continue

        price = description.find_next("div", class_=["realty-preview-price", "realty-preview-price--main"]). \
            text.replace("\xa0", "")

        address = description.find_next("h3", class_="realty-preview-title"). \
            find_next("a", class_="realty-preview-title__link").text

        list_of_addresses = [item.text for item in description.find_all("a", class_="realty-preview-sub-title")]
        result_addresses = ", ".join(list_of_addresses)

        description_text = description.find_next("p", class_="realty-preview-description__text").text

        properties = {prop.find_next("span").text
                      for prop in description.find_all(class_="realty-preview-properties-item")}
        props_text = "; ".join(properties)

        city = City.objects(city_id=city_id)[0]

        if not len(Notice.objects(notice_id=article_id)):
            Notice(notice_id=article_id,
                   image_url=picture,
                   description=description_text,
                   price=int(price.split(" ")[0]),
                   address=address,
                   full_address=result_addresses,
                   properties=props_text,
                   city=city,
                   creation_date=datetime.now()).save()
            logging.info(f"added notice: {article_id} {city.city_name} {result_addresses}")
