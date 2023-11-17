from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver import Keys

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

url = ("https://market.lun.ua/uk/search?currency=USD&geo_id=26&is_without_fee=false&price_sqm_currency=USD&section_id=1"
       "&sort=relevance&without_broker=owner")

driver.implicitly_wait(3)

driver.get(url)

page_height = driver.execute_script('return document.body.scrollHeight;')
window_height = driver.execute_script("return window.screen.height;")

total_height = 0

while total_height < driver.execute_script('return document.body.scrollHeight;'):
    driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.PAGE_DOWN)
    driver.implicitly_wait(1)

    total_height += window_height

src = driver.page_source

driver.quit()

soup = BeautifulSoup(src, "lxml")

list_of_articles = soup.find_all("img")
for article in list_of_articles:
    # pictures = article.find_next("img")
    print(article)

