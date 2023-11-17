import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

url = ("https://market.lun.ua/uk/search?currency=USD&geo_id=26&is_without_fee=false&price_sqm_currency=USD&section_id=1"
       "&sort=relevance&without_broker=owner")

# headers = {
#     "Accept": "*/*",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 "
#                   "Safari/537.36"
# }

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)
driver.maximize_window()

# wait = WebDriverWait(driver, 10)

driver.get(url)

# check_height = driver.execute_script("return document.body.scrollHeight;")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     try:
#         wait.until(lambda d: driver.execute_script("return document.body.scrollHeight;") > check_height)
#         check_height = driver.execute_script("return document.body.scrollHeight;")
#     except TimeoutException:
#         break

# driver.implicitly_wait(1)

# driver.implicitly_wait(10)

src = driver.page_source

# req = requests.get(url=url, headers=headers)
# src = req.text

# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(str(src))

soup = BeautifulSoup(src, "html.parser")

list_of_articles = soup.find_all(class_="realty-preview__base")
for article in list_of_articles:
    # print(article)
    # article_photos = article.find_next("picture", class_="realty-preview__image")
    article_photos = article.find_next(name="img")

    print(article_photos)
    # article_descr = article.find_next(class_="realty-preview__content-column")
    # print(article_descr)

# print(src)


# def main():
#     pass
#
#
# if __name__ == '__main__':
#     main()
