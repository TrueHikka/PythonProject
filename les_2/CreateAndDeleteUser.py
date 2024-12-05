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
        driver.get("https://opensource-demo.orangehrmlive.com/")
        time.sleep(3)  # Явное ожидание загрузки страницы

        # Находим и заполняем логин
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Admin")

        # Находим и заполняем пароль
        password = driver.find_element(By.NAME, "password")
        password.send_keys("admin123")

        # Находим и кликаем кнопку входа
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        time.sleep(3)  # Ожидание загрузки после входа
        print("Успешная авторизация")

    except Exception as e:
        print(f"Ошибка при входе: {e}")
        driver.save_screenshot("login_error.png")
        raise

def create_employee(driver):
    try:
        # Переход в PIM
        pim_menu = driver.find_element(By.LINK_TEXT, "PIM")
        pim_menu.click()
        time.sleep(2)

        # Переход к добавлению сотрудника
        add_employee = driver.find_element(By.LINK_TEXT, "Add Employee")
        add_employee.click()
        time.sleep(2)

        # Заполнение формы
        first_name = driver.find_element(By.NAME, "firstName")
        first_name.send_keys("Vladimir")

        middle_name = driver.find_element(By.NAME, "middleName")
        middle_name.send_keys("Vladimirov")

        last_name = driver.find_element(By.NAME, "lastName")
        last_name.send_keys("Vladimirovich")

        # Генерация ID
        first_initial = first_name.get_attribute("value")[0]
        middle_initial = middle_name.get_attribute("value")[0]
        last_initial = last_name.get_attribute("value")[0]
        initials = first_initial + middle_initial + last_initial

        # Работа с ID сотрудника
        employee_id_element = driver.find_element(By.CSS_SELECTOR, ".oxd-grid-2 .oxd-input")
        employee_id = employee_id_element.get_attribute("value")

        # Генерация нового ID
        new_employee_id = employee_id + initials

        # Очистка поля ID и заполнение поля новым ID
        employee_id_element.click()
        employee_id_element.send_keys(Keys.CONTROL + "a")
        employee_id_element.send_keys(Keys.DELETE)
        employee_id_element.send_keys(new_employee_id)

        # Сохранение
        save_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        save_button.click()

        time.sleep(3)

        print(f"Сотрудник {new_employee_id} создан успешно")

        return new_employee_id

    except Exception as e:
        print(f"Ошибка при создании сотрудника: {e}")
        driver.save_screenshot("create_employee_error.png")
        raise

def delete_employee(driver, employee_id):
    try:
        # Переход в список сотрудников
        employee_list = driver.find_element(By.LINK_TEXT, "Employee List")
        employee_list.click()
        time.sleep(3)

        # Найти все поля ввода
        input_fields = driver.find_elements(By.CSS_SELECTOR, ".oxd-input")

        # Найти второе текстовое поле ввода
        if len(input_fields) > 1:
            search_input = input_fields[1]
            search_input.clear()
            search_input.send_keys(employee_id)
            time.sleep(2)

        # Кнопка поиска
        search_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")

        if search_buttons:
            search_buttons[0].click()
            time.sleep(2)

        # Поиск чекбокса для выбора сотрудника
        checkboxes = driver.find_elements(By.CSS_SELECTOR, ".oxd-table.orangehrm-employee-list .oxd-table-card-cell-checkbox")

        if checkboxes:
            checkboxes[0].click()
            time.sleep(1)

        # Найти кнопку удаления
        delete_button = driver.find_elements(By.CSS_SELECTOR, "button.oxd-button--label-danger")

        if delete_button:
            delete_button[0].click()
            time.sleep(1)

            # Подтверждение удаления
            confirm_button = driver.find_elements(By.CSS_SELECTOR, ".orangehrm-modal-footer button.oxd-button--label-danger")

            if confirm_button:
                confirm_button[0].click()
                print(f"Сотрудник с ID {employee_id} успешно удален")
                time.sleep(3)
            else:
                print("Не удалось найти кнопку подтверждения удаления")
        else:
            print("Не удалось найти кнопку удаления")

    except Exception as e:
        print(f"Ошибка при удалении сотрудника: {e}")
        driver.save_screenshot("delete_employee_error.png")
        raise

def main():
    driver = None
    try:
        driver = create_driver()
        login(driver)
        employee_id = create_employee(driver)
        delete_employee(driver, employee_id)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()