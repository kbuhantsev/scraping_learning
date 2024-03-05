from selenium.webdriver import Keys, ChromeOptions, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def main():
    url = "https://dom.ria.com/uk/search/?excludeSold=1&category=1&realty_type=2&operation=1&state_id=12&price_cur=1\
    &wo_dupl=1&sort=inspected_sort&period=per_allday&firstIteraction=false&city_ids=12&client=searchV2&limit=20\
    &type=list&ch=242_239,247_252,1437_1436"

    service = Service(ChromeDriverManager().install())

    options = ChromeOptions()
    options.add_argument("headless")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = Chrome(service=service, options=options)

    driver.maximize_window()

    driver.get(url)
    driver.implicitly_wait(0.5)

    src = driver.page_source
    with open("data.html", "w", encoding="utf-8") as file:
        file.write(src)


if __name__ == "__main__":
    main()
