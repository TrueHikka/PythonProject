import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def create_driver():
    # Создание опций для Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Открытие браузера в полноэкранном режиме
    chrome_options.add_argument("--no-sandbox")  # Отключение sandbox режима для стабильности
    chrome_options.add_argument("--disable-dev-shm-usage")  # Решение проблем с памятью в некоторых средах
    chrome_options.add_argument("--remote-debugging-port=9222")  # Порт для удаленной отладки

    # Автоматическая установка актуального ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Создание экземпляра драйвера Chrome с указанными опциями
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Неявное ожидание - драйвер будет ждать до 10 секунд при поиске элементов
    driver.implicitly_wait(10)

    return driver

def login(driver):
    try:
        driver.get("https://www.saucedemo.com/")
        time.sleep(3)

        credentials_elements = driver.find_element(By.ID, "login_credentials")

        # Получаем текст элемента
        credentials_text = credentials_elements.text

        # Разделяем текст на строки
        credentials_list = credentials_text.split('\n')

        # Найти и заполнить поля логина и пароля
        username_input = driver.find_element(By.ID, "user-name")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        # Используем первый логин из списка
        username_input.send_keys(credentials_list[1])
        password_input.send_keys("secret_sauce")
        login_button.click()

        time.sleep(3)

        print("Успешная авторизация")

    except Exception as e:
        print(f"Ошибка при входе: {e}")
        driver.save_screenshot("login_error.png")
        raise

def add_items_to_cart(driver, num_items):
    try:
        # Находим все карточки товаров
        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")

        # Счетчик добавленных товаров
        added_items = 0

        for item in inventory_items:
            # Если уже добавили нужное количество - выходим
            if added_items >= num_items:
                break

            # Находим кнопку добавления
            add_to_cart_button = item.find_element(By.CLASS_NAME, "btn_inventory")

            # Добавляем товар
            add_to_cart_button.click()

            # Увеличиваем счетчик
            added_items += 1

            time.sleep(0.5)

        print("Товары успешно добавлены в корзину")

    except Exception as e:
        print(f"Ошибка при добавлении товара в корзину: {e}")
        driver.save_screenshot("add_to_cart_error.png")
        raise

def checking_count_items_in_cart(driver, num_items):
    try:
        # Находим элемент счетчика товаров в корзине
        shopping_cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        shopping_cart_button.click()
        time.sleep(1)

        # Находим список товаров в корзине
        cart_list = driver.find_element(By.CLASS_NAME, "cart_list")

        # Находим все товары в корзине
        cart_items = cart_list.find_elements(By.CLASS_NAME, "cart_item")

        # Проверяем, что количество товаров в корзине соответствует заданному числу
        if len(cart_items) == num_items:
            print("Количество товаров в корзине соответствует заданному числу")
            return True
        else:
            print(f"Количество товаров в корзине ({len(cart_items)}) не соответствует заданному числу ({num_items})")
            return False


        # ИЛИ ТАК
        # cart_list = driver.find_element(By.CLASS_NAME, "cart_list")
        #
        # sum_count_items = 0
        #
        # cart_items = cart_list.find_elements(By.CLASS_NAME, "cart_item")
        #
        # for item in cart_items:
        #     count_items = int(item.find_element(By.CLASS_NAME, "cart_quantity").text)
        #     sum_count_items += count_items
        #
        # if sum_count_items == num_items:
        #     print("Количество товаров в корзине соответствует заданному числу")
        #     return True
        # else:
        #     print("Количество товаров в корзине не соответствует заданному числу")
        #     return False

    except Exception as e:
        print(f"Ошибка при проверке количества товаров в корзине: {e}")
        driver.save_screenshot("check_cart_error.png")
        raise

def main():
    driver = None
    try:
        driver = create_driver()
        login(driver)
        num_items = 2
        add_items_to_cart(driver, num_items)
        checking_count_items_in_cart(driver, num_items)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()