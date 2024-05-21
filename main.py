import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

url = "https://www.divan.ru/category/svet"
driver.get(url)

time.sleep(5)

try:
    lights = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.lcSMD'))
    )
except Exception as e:
    print(f"Не удалось найти товар: {e}")
    driver.quit()
    exit(1)

parsed_data = []

for light in lights:
    try:

        title_element = light.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]')
        price_element = light.find_element(By.CSS_SELECTOR, 'span[data-testid="price"]')
        link_element = light.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8')

        title = title_element.text
        price = price_element.text
        link = link_element.get_attribute('href')

        print(f"Title: {title}, Price: {price}, Link: {link}")

        parsed_data.append([title, price, link])

    except Exception as e:
        print(f"Произошла ошибка при парсинге данных: {e}")
        continue

driver.quit()

if not parsed_data:
    print("Нет данных для записи в CSV")
else:
    print("Собрано данных для записи: ", len(parsed_data))

try:
    with open('light.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        writer.writerows(parsed_data)
    print("Данные успешно сохранены в light.csv")
except Exception as e:
    print(f"Произошла ошибка при записи данных в CSV: {e}")
