from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrolldown(driver, times=50):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(0.1)

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Можно убрать для визуализации
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/opt/homebrew/bin/chromedriver")
    return webdriver.Chrome(service=service, options=chrome_options)

def get_mainpage_cards(driver, url):
    driver.get(url)
    scrolldown(driver, 50)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    content = soup.select_one("div.category-block.cars")
    if not content:
        print("[ERROR] Не найден блок category-block.cars")
        return []

    contents = content.select("div.category-block-content")
    if not contents:
        print("[ERROR] Не найдены div с классом category-block-content")
        return []

    all_cards = []
    for layer in contents:
        cards = layer.find_all("div", recursive=False)
        for card in cards:
            link = card.select_one("a[href]")
            if link:
                href = link['href']
                product_url = "https://m.mashina.kg/" + href.lstrip("/")
                all_cards.append(product_url)

    return all_cards

if __name__ == "__main__":
    driver = create_driver()
    try:
        cards = get_mainpage_cards(driver, "https://m.mashina.kg/en/")
        print(f"[INFO] Найдено  : {len(cards)}")
        for c in cards:
            print(c)
    finally:
        driver.quit()
