import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import choice


browser = webdriver.Firefox()
url = 'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
browser.get(url)

assert "Википедия" in browser.title
time.sleep(3)
search_box = browser.find_element(By.ID, "searchInput")
search_box.send_keys("Солнечная система")
search_box.send_keys(Keys.RETURN)
time.sleep(3)
link = browser.find_element(By.LINK_TEXT, "Солнечная система")
link.click()

# Бегаем по параграфам
paragraphs = browser.find_elements(By.TAG_NAME, "p")

for paragraph in paragraphs:
    print(paragraph.text)
    input()

hat_notes = []

for element in browser.find_elements(By.TAG_NAME, 'div'):
    cl = element.get_attribute("class")
    if cl == "hatnote navigation-not-searchable":
        hat_notes.append(element)

print(hat_notes)

hat_notes = choice(hat_notes)
link = hat_notes.find_element(By.TAG_NAME, "a").get_attribute("href")
browser.get(link)

