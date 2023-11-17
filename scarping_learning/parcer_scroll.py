from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(service=service, options=options)

url = ("https://market.lun.ua/uk/search?currency=USD&geo_id=26&is_without_fee=false&price_sqm_currency=USD&section_id=1"
       "&sort=relevance&without_broker=owner")

driver.get(url)


driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.implicitly_wait(10)

src = driver.page_source

soup = BeautifulSoup(src, "lxml")

list_of_articles = soup.find_all("div", "realty-preview__base")
for article in list_of_articles:
    pictures = article.find_next("img")
    print(pictures)


