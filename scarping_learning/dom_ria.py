# from selenium import webdriver
import json
from pprint import pprint

from selenium_stealth import stealth
from fake_useragent import UserAgent

from seleniumwire import webdriver
from seleniumwire.utils import decode

import time
import gzip


def my_response_interceptor(request, response):
    if request.url.startswith("https://dom.ria.com/realty/data/"):
        # print(request.url, response.body.decode("utf-8"))
        # body = json.loads(gzip.decompress(response.body).decode("utf-8"))
        body = json.loads(
            decode(response.body, response.headers.get("Content-Encoding", "identity"))
        )
        pprint(body)


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

    url = "https://dom.ria.com/uk/search/?excludeSold=1&category=1&realty_type=2&operation=3&state_id=12&price_cur=1&wo_dupl=1&sort=inspected_sort&period=per_allday&firstIteraction=false&city_ids=12&client=searchV2&type=list&limit=20&ch=226_223,246_244,1437_1436%3A"

    driver.response_interceptor = my_response_interceptor

    driver.get(url)

    time.sleep(5)

    src = driver.page_source
    with open("data.html", "w", encoding="utf-8") as file:
        file.write(src)

    driver.quit()


if __name__ == "__main__":

    get_page_soup()
