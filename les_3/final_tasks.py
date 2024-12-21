import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup

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

def wait_for_element(driver, locator, timeout=10, condition=EC.presence_of_element_located):
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Начало поиска элемента: {locator}")
        start_time = time.time()

        # Периодическая проверка условия condition для элемента locator
        # Ждем, пока условие не станет истинным
        # Возвращаем найденный элемент, если условие выполнено
        element = WebDriverWait(driver, timeout).until(
            condition(locator)
        )

        wait_time = time.time() - start_time
        print(f"[{time.strftime('%H:%M:%S')}] Элемент найден за {wait_time:.2f} сек")

        return element

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка поиска элемента: {e}")
        driver.save_screenshot(f"element_error_{int(time.time())}.png")
        raise
#
#! Task 1
def explicit_expectation(driver):
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Начало теста")
        driver.get("http://demo.automationtesting.in/WebTable.html")

        more_link = wait_for_element(driver, (By.LINK_TEXT, "More"))
        more_link.click()

        loader_link = wait_for_element(driver, (By.LINK_TEXT, "Loader"))
        loader_link.click()

        run_btn = wait_for_element(
            driver,
            (By.XPATH, "//button[contains(text(), 'Run')]"),
            condition=EC.element_to_be_clickable
        )
        run_btn.click()

        # Ждем появления модального окна
        modal = wait_for_element(
            driver,
            (By.CSS_SELECTOR, ".modal-body"),
            timeout=15
        )

        # Ждем появления текста со словом "Lorem" в элементе p
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".modal-body p"), "Lorem")
        )

        # Проверяем текст внутри элемента
        lorem_text = modal.find_element(By.CSS_SELECTOR, "p")
        assert "Lorem" in lorem_text.text, f"[{time.strftime('%H:%M:%S')}] Текст 'Lorem' не найден. Текущий текст: {lorem_text.text}"
        print(f"[{time.strftime('%H:%M:%S')}] Слово 'Lorem' найдено в модальном окне")

        save_changes_btn = wait_for_element(
            driver,
            (By.CSS_SELECTOR, ".modal-footer .btn-primary"),
            condition=EC.element_to_be_clickable
        )
        save_changes_btn.click()

        print(f"[{time.strftime('%H:%M:%S')}] Тест успешно завершен")

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

#! Task 2
def implicit_expectation(driver):
    driver.implicitly_wait(5)
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Начало теста")
        driver.get("http://demo.automationtesting.in/WebTable.html")
        more_link = driver.find_element(By.LINK_TEXT, "More")
        more_link.click()

        dinamic_data_link = driver.find_element(By.LINK_TEXT, "Dynamic Data")
        dinamic_data_link.click()

        h3_elem = driver.find_element(By.TAG_NAME, "h3")

        if h3_elem.text != "Loading the data Dynamically":
            print(f"[{time.strftime('%H:%M:%S')}] Текст заголовка не соответствует ожидаемому")
            driver.save_screenshot(f"test_error_{int(time.time())}.png")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Текст заголовка соответствует ожидаемому")

            btn_default = driver.find_element(By.CLASS_NAME, "btn-default")
            btn_default.click()

            time.sleep(3)

            img_elem = driver.find_element(By.TAG_NAME, "img")
            img_src = img_elem.get_attribute("src")
            print(f"[{time.strftime('%H:%M:%S')}] Ссылка на изображение: {img_src}")

            print(f"[{time.strftime('%H:%M:%S')}] Тест успешно завершен")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

#! Task 3
def second_implicit_expectation(driver):
    driver.implicitly_wait(5)
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Начало теста")
        driver.get("http://demo.automationtesting.in/WebTable.html")
        more_link = driver.find_element(By.LINK_TEXT, "More")
        more_link.click()

        file_upload_link = driver.find_element(By.LINK_TEXT, "File Upload")
        file_upload_link.click()

        input_select_file = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        input_select_file.send_keys(r"C:\Users\Lenovo\OneDrive\Рабочий стол\wallpaper\halloween-scene-illustration-anime-style.jpg")

        remove_btn = driver.find_element(By.CSS_SELECTOR, "button.fileinput-remove-button")
        remove_btn.click()

        file_name = r'C:\Users\Lenovo\OneDrive\Рабочий стол\test.txt'
        with open(file_name, 'w'):
            pass

        input_select_file = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        input_select_file.send_keys(file_name)

        error_block = driver.find_element(By.CSS_SELECTOR, "div.file-error-message")
        if error_block.is_displayed():
            # Получение HTML-кода элемента
            html_content = error_block.get_attribute('outerHTML')

            # Парсинг HTML-кода
            soup = BeautifulSoup(html_content, 'html.parser')

            # Удаление элемента <span>
            span = soup.find('span', class_='close kv-error-close')
            if span:
                span.decompose()

            # Получение текста без HTML-тегов и пробелов
            error_text = soup.get_text(strip=True)

            print(f"[{time.strftime('%H:%M:%S')}] Ошибка: {error_text}")

            close_span = driver.find_element(By.CSS_SELECTOR, ".close.kv-error-close")
            close_span.click()

        upload_btn = driver.find_element(By.CSS_SELECTOR, "button.fileinput-upload-button")
        if upload_btn.get_attribute('disabled'):
            print(f"[{time.strftime('%H:%M:%S')}] Кнопка Upload отключена")

        print(f"[{time.strftime('%H:%M:%S')}] Тест успешно завершен")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

#! Task 4
def explicit_and_implicit_expectation(driver):
    driver.implicitly_wait(10)
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Начало теста")
        driver.get("http://demo.automationtesting.in/WebTable.html")

        # Перейдите в раздел "More" -> "JQuery ProgressBar"
        more_link = driver.find_element(By.LINK_TEXT, "More")
        more_link.click()

        jquery_progressbar_link = driver.find_element(By.LINK_TEXT, "JQuery ProgressBar")
        jquery_progressbar_link.click()

        # Реализуйте явное ожидание для проверки, что кнопка "Close" невидима
        close_button_locator = (By.XPATH, "//button[text()='Cancel']")
        wait_for_element(driver, close_button_locator, condition=EC.invisibility_of_element_located)

        # Нажмите кнопку "Start Download"
        start_download_button = driver.find_element(By.CSS_SELECTOR, "button#downloadButton")
        start_download_button.click()

        # Реализуйте явное ожидание для проверки, что кнопка называется "Cancel Download"
        cancel_download_button_locator = (By.XPATH, "//button[text()='Cancel Download']")
        wait_for_element(driver, cancel_download_button_locator)

        # Закройте окно. Снова откройте
        close_button = driver.find_element(By.CSS_SELECTOR, ".ui-dialog-buttonset button")
        close_button.click()

        # Нажмите кнопку "Start Download" снова
        start_download_button = driver.find_element(By.CSS_SELECTOR, "button#downloadButton")
        start_download_button.click()

        # Реализуйте явное ожидание для проверки, что в окне присутствует текст "Complete!"
        complete_text_locator = (By.XPATH, "//div[text()='Complete!']")
        wait_for_element(driver, complete_text_locator)

        print(f"[{time.strftime('%H:%M:%S')}] Тест успешно завершен")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

#! Task 5
def second_explicit_and_implicit_expectation(driver):
    driver.implicitly_wait(10)
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Начало теста")
        driver.get("http://demo.automationtesting.in/WebTable.html")

        # Перейдите в раздел "Switch to" -> "Windows"
        switch_to_link = driver.find_element(By.LINK_TEXT, "SwitchTo")
        switch_to_link.click()

        windows_link = driver.find_element(By.LINK_TEXT, "Windows")
        windows_link.click()

        # В разделе "Open New Tabbed Windows" нажмите кнопку "click"
        open_new_tab_button = driver.find_element(By.CSS_SELECTOR, "a .btn-info")
        open_new_tab_button.click()

        # Переключите драйвер на вторую вкладку
        handles = driver.window_handles
        driver.switch_to.window(handles[1])

        # Закройте её
        driver.close()

        # Переключитесь обратно на первую вкладку
        driver.switch_to.window(handles[0])

        # Перейдите в раздел "Separate Multiple Windows" и нажмите "click"
        separate_multiple_windows_link = driver.find_element(By.LINK_TEXT, "Open Seperate Multiple Windows")
        separate_multiple_windows_link.click()

        multiple_windows_button = driver.find_element(By.CSS_SELECTOR, ".tab-content .btn-info:nth-child(2)")
        multiple_windows_button.click()

        # Переключите драйвер на вторую вкладку
        handles = driver.window_handles
        driver.switch_to.window(handles[2])

        wait = WebDriverWait(driver, 10)

        # Используя явное ожидание(EC), проверьте что ссылка = "http://demo.automationtesting.in/Index.html"
        wait.until(EC.url_to_be("https://demo.automationtesting.in/Index.html"))

        # Используя явное ожидание(EC), проверьте что в браузере открыто 3 вкладки, выведите в консоли результат проверки (True/False)
        wait.until(lambda driver: len(driver.window_handles) == 3)
        print(f"[{time.strftime('%H:%M:%S')}] В браузере открыто 3 вкладки: {len(driver.window_handles) == 3}")

        # В поле "email" напишите любую почту и нажмите на кнопку в виде ">" справа от поля
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("test@example.com")

        submit_button = driver.find_element(By.ID, "enterimg")
        submit_button.click()

        # Используя явное ожидание(EC), проверьте что ссылка = "http://demo.automationtesting.in/Register.html"
        wait.until(EC.url_to_be("https://demo.automationtesting.in/Register.html"))

        print(f"[{time.strftime('%H:%M:%S')}] Тест успешно завершен")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def main():
    driver = None
    try:
        driver = create_driver()
        explicit_expectation(driver)
        implicit_expectation(driver)
        second_implicit_expectation(driver)
        explicit_and_implicit_expectation(driver)
        second_explicit_and_implicit_expectation(driver)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Критическая ошибка: {e}")
    finally:
        if driver:
            driver.quit()
            print(f"[{time.strftime('%H:%M:%S')}] Драйвер закрыт")
if __name__ == "__main__":
    main()