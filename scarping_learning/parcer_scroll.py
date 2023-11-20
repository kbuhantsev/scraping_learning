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

url = ("https://market.lun.ua/uk/search?currency=USD&geo_id=26&is_without_fee=false&page=1&price_sqm_currency=USD&\
section_id=1&sort=insert_time&without_broker=owner")

# section_id=1 - квартиры
# section_id=2 - аренда квартир
# section_id=3 - дома
# section_id=4 - аренда домов


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

list_of_articles = soup.find_all("article")
for article in list_of_articles:

    print("ID: " + article.get("id"))

    picture = article.find_next("picture", class_="realty-preview__image").find_next("img").get("src")
    print("картинка: ", picture)

    description = article.find_next(class_="realty-preview__content-column")
    # print(description)
    price = (description.find_next("div", class_=["realty-preview-price", "realty-preview-price--main"]).
             text.replace("\xa0", ""))
    print(price)

    address = (description.find_next("h3", class_="realty-preview-title").
               find_next("a", class_="realty-preview-title__link")
               .text)
    print(address)

    list_of_addresses = description.find_all("a", class_="realty-preview-sub-title")
    result_addresses = ""
    for item in list_of_addresses:
        result_addresses += item.text + ", "
    result_addresses = result_addresses[0:len(result_addresses)-2]
    print(result_addresses)

    description_text = description.find_next("p", class_="realty-preview-description__text").text
    print(description_text)

    properties = description.find_all(class_="realty-preview-properties-item")
    for prop in properties:
        value = prop.find_next("span").text
        print(value)

    break

