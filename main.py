import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def search_wikipedia(browser, query):
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

def get_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        if paragraph.text.strip():
            print(f"Параграф {i + 1}:\n{paragraph.text}\n")
            user_input = input("Нажмите Enter для перехода к следующему параграфу или введите 'stop', чтобы остановиться: ")
            if user_input.lower() == 'stop':
                break

def get_internal_links(browser):
    links = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/wiki/"]')
    unique_links = {}
    for link in links:
        text = link.text.strip()
        href = link.get_attribute("href")
        if text and href not in unique_links:
            unique_links[href] = text
    return unique_links

def choose_link(links):
    if not links:
        print("Связанных статей не найдено.")
        return None
    print("\nДоступные связанные статьи:")
    for i, (href, text) in enumerate(links.items(), start=1):
        print(f"{i}. {text} ({href})")
    while True:
        try:
            choice = int(input("\nВведите номер статьи для перехода или 0 для отмены: "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(links):
                return list(links.keys())[choice - 1]
            else:
                print("Некорректный ввод. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def main():
    browser = webdriver.Firefox()
    url = 'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
    browser.get(url)
    assert "Википедия" in browser.title
    time.sleep(3)

    try:
        while True:
            query = input("Введите запрос для поиска в Википедии (или 'exit' для выхода): ")
            if query.lower() == 'exit':
                print("Выход из программы.")
                break

            search_wikipedia(browser, query)

            while True:
                print("\nВыберите действие:")
                print("1. Просмотреть параграфы текущей статьи.")
                print("2. Перейти на связанную статью.")
                print("3. Вернуться к новому запросу.")
                print("4. Выйти из программы.")

                choice = input("Введите номер действия: ")

                if choice == '1':
                    get_paragraphs(browser)
                elif choice == '2':
                    links = get_internal_links(browser)
                    new_url = choose_link(links)
                    if new_url:
                        browser.get(new_url)
                        time.sleep(3)
                    else:
                        print("Возврат к предыдущему меню.")
                elif choice == '3':
                    break
                elif choice == '4':
                    print("Выход из программы.")
                    return
                else:
                    print("Некорректный ввод. Попробуйте снова.")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
