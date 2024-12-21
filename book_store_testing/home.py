import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    return driver

def adding_comment(driver):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        driver.execute_script("window.scrollBy(0, 600);")

        h3_header = driver.find_element(By.XPATH, "//h3[text()='Selenium Ruby']")
        h3_header.click()

        time.sleep(3)

        driver.execute_script("window.scrollBy(0, 500);")

        reviews_link = driver.find_element(By.CSS_SELECTOR, ".tabs .reviews_tab a")
        reviews_link.click()

        time.sleep(3)

        rating_span = driver.find_element(By.CSS_SELECTOR, ".stars span")

        stars = rating_span.find_elements(By.TAG_NAME, "a")

        if len(stars) >= 5:
            star_5 = stars[4]

            if 'active' not in star_5.get_attribute('class'):
                star_5.click()

                time.sleep(3)

                #! Пример вывода: [14:30:45] Оценка 5 звезд
                print("[{}] Оценка 5 звезд теперь активна".format(time.strftime('%H:%M:%S')))
            else:
                print("[{}] Оценка 5 звезд уже активна".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Количество звезд меньше 5".format(time.strftime('%H:%M:%S')))

        textarea_comment = driver.find_element(By.ID, "comment")
        textarea_comment.click()

        current_text = textarea_comment.get_attribute('value')

        if current_text:
            textarea_comment.clear()
            print("[{}] Текст комментария очищен".format(time.strftime('%H:%M:%S')))

        new_comment = "Nice book"

        textarea_comment.send_keys(new_comment)

        time.sleep(3)

        driver.execute_script("window.scrollBy(0, 250);")

        input_name = driver.find_element(By.ID, "author")
        input_name.click()

        current_name = input_name.get_attribute('value')

        if current_name:
            input_name.clear()
            print("[{}] Имя очищено".format(time.strftime('%H:%M:%S')))

        new_name = "Vladimir"

        input_name.send_keys(new_name)

        time.sleep(3)

        email_input = driver.find_element(By.ID, "email")
        email_input.click()

        current_email = email_input.get_attribute('value')

        if current_email:
            email_input.clear()
            print("[{}] Почта очищена".format(time.strftime('%H:%M:%S')))

        new_email = "5rY7t@example.com"

        email_input.send_keys(new_email)

        time.sleep(3)

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        print("[{}] Комментарий добавлен".format(time.strftime('%H:%M:%S')))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def main():
    driver = None
    try:
        driver = create_driver()
        adding_comment(driver)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Критическая ошибка: {e}")
    finally:
        if driver:
            driver.quit()
            print(f"[{time.strftime('%H:%M:%S')}] Драйвер закрыт")
if __name__ == "__main__":
    main()