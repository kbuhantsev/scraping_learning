# from selenium import webdriver
import json

from selenium_stealth import stealth
from fake_useragent import UserAgent

from seleniumwire import webdriver

import time
import gzip


def my_response_interceptor(request, response):
    if request.url.startswith("https://dom.ria.com/realty/data/"):
        # print(request.url, response.body.decode("utf-8"))
        body = gzip.decompress(response.body)
        print(body.decode("utf-8"))


def get_page_soup():

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(
        options=options,
    )

    user_agent = UserAgent()

    stealth(
        driver,
        user_agent=user_agent.random,
        languages=["uk-UK", "uk"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    url = "https://dom.ria.com/uk/search/?excludeSold=1&category=1&realty_type=2&operation=1&state_id=12&price_cur=1&wo_dupl=1&sort=inspected_sort&period=per_allday&firstIteraction=false&city_ids=12&client=searchV2&limit=20&type=list&ch=226_223,246_244,1437_1436%3A"

    driver.response_interceptor = my_response_interceptor

    driver.get(url)

    # for request in driver.requests:
    #     if request.response:
    #         if request.url.startswith("https://dom.ria.com/realty/data/"):
    #             print(request.url, json.loads(request.response.body))

    time.sleep(5)

    src = driver.page_source
    with open("data.html", "w", encoding="utf-8") as file:
        file.write(src)

    driver.quit()


if __name__ == "__main__":

    cities = []

    # realty_type 2 - квартиры, 0 - дома
    operations = [1, 3]  # operation 1 - продажа, 3 - аренда
    categories = [1, 4]  # category 1 - квартиры, 4 - дома

    get_page_soup()
