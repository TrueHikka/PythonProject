import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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
    driver.implicitly_wait(10)

    return driver

def login(driver):
    try:
        driver.get("https://demo.us.espocrm.com/")
        time.sleep(3)

        element = driver.find_element(By.CSS_SELECTOR, "#login-form .form-group:nth-child(2) .form-control")
        select = Select(element)
        select.select_by_value("en_US")

        login_button = driver.find_element(By.ID, "btn-login")
        login_button.click()

        print("Успешная авторизация")
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при открытии страницы: {e}")
        driver.save_screenshot("login_error.png")
        raise

#! 2-3
def open_tasks_section(driver):
    try:
        # Нажатие на "Activities" в левом меню
        elem_li = driver.find_element(By.CSS_SELECTOR, ".navbar-collapse ul li:nth-child(7) .label-text")
        if elem_li == 'Activities':
            print("Открыт раздел \"Activities\"")

        # Нажатие на "Tasks"
        span_tasks = driver.find_element(By.LINK_TEXT, "Tasks")
        span_tasks.click()
        print("Открыт раздел \"Tasks\"")
        time.sleep(3)

        # Выбор селектора "All"
        selector_btn = driver.find_element(By.CSS_SELECTOR, ".form-group button")
        selector_btn.click()
        print("Выбран селектор \"All\"")
        time.sleep(3)

    except Exception as e:
        print(f"Ошибка при открытии раздела \"Tasks\": {e}")
        driver.save_screenshot("tasks_error.png")
        raise
#! 4
def filter_tasks(driver):
    try:
        #Отметить чекбокс "Only My"
        checkbox = driver.find_element(By.CSS_SELECTOR, "li.checkbox:nth-child(11)")
        checkbox.click()
        print("Отмечен чекбокс \"Only My\"")
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при отметке чекбокса \"Only My\": {e}")
        driver.save_screenshot("checkbox_error.png")
        raise
#! 5-7
def task_selection_and_mass_actions(driver):
    try:
        # Выбор всех задач или создание задачи
        table_body = driver.find_element(By.CSS_SELECTOR, "tbody")
        rows = table_body.find_elements(By.CSS_SELECTOR, "tr")

        if len(rows) > 0:
            print("Список задач не пуст")

            input_all = driver.find_element(By.CSS_SELECTOR, ".select-all-container .select-all")
            input_all.click()

            print("Выбраны все задачи")

            time.sleep(3)
        else:
            print("Список задач пуст")

            create_task_button = driver.find_element(By.LINK_TEXT, "Create Task")
            create_task_button.click()
            time.sleep(3)

            input_name = driver.find_element(By.CSS_SELECTOR,".field input[type='text']")
            input_name.send_keys("Test")

            save_btn = driver.find_element(By.CSS_SELECTOR, ".record .btn-group .btn:nth-child(1)")
            save_btn.click()
            print("Задача создана")
            time.sleep(3)

            tasks_link = driver.find_element(By.LINK_TEXT, "Tasks")
            tasks_link.click()
            time.sleep(3)

        # Нажатие "Actions" и выбор "Mass Update"
        action_btn = driver.find_element(By.CSS_SELECTOR, ".list-buttons-container .btn-group.actions button[type='button']")
        action_btn.click()
        time.sleep(3)

        mass_update_btn = driver.find_element(By.LINK_TEXT, "Mass Update")
        mass_update_btn.click()
        print("Выбрана массовая обновление задач")
        time.sleep(3)

        # Проверка недоступности кнопки "Update"
        update_btn = driver.find_element(By.CLASS_NAME, "btn-danger")
        if update_btn.is_enabled():
            print("Кнопка 'Update' доступна")
        else:
            print("Кнопка 'Update' недоступна")
            close_link = driver.find_element(By.CLASS_NAME, "close")
            close_link.click()
            print("Закрытие окна")
            time.sleep(3)

    except Exception as e:
        print(f"Ошибка при выполнении задания: {e}")
        driver.save_screenshot("task_error.png")
        raise
#! 8-10
def create_new_task(driver):
    try:
        # Нажатие "Create Task"
        create_task_button = driver.find_element(By.LINK_TEXT, "Create Task")
        create_task_button.click()
        time.sleep(5)

        # Заполнение поля "Name" значением "Test"
        input_name = driver.find_element(By.XPATH,"//input[@data-name='name']")
        input_name.send_keys("Test")

        # Проверка статуса "Not Started"
        status_select = driver.find_element(By.CSS_SELECTOR, ".col-sm-6:nth-child(1) select")
        select = Select(status_select)
        selected_option = select.first_selected_option
        if selected_option.text == "Not Started":
            print("Статус задачи 'Not Started'")
        else:
            print("Статус задачи не 'Not Started'")

        # Сохранение задачи
        save_btn = driver.find_element(By.CSS_SELECTOR, ".btn-xs-wide:nth-child(1)")
        save_btn.click()
        print("Задача создана")
        time.sleep(3)

        # Возврат в список задач
        tasks_link = driver.find_element(By.LINK_TEXT, "Tasks")
        tasks_link.click()
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при создании новой задачи: {e}")
        driver.save_screenshot("create_task_error.png")
        raise


#! 11-13
def remove_task(driver):
    try:
        # Выбор первой задачи в списке
        first_checkbox = driver.find_element(By.CSS_SELECTOR, ".list-row:nth-child(1) input[type='checkbox']")
        first_checkbox.click()
        print("Выбрана первая задача")
        time.sleep(3)

        # Нажатие "Actions" и Выбор "Remove"
        action_btn = driver.find_element(By.CSS_SELECTOR, ".list-buttons-container .btn-group.actions button[type='button']")
        action_btn.click()
        time.sleep(3)

        remove_link = driver.find_element(By.LINK_TEXT, "Remove")
        remove_link.click()
        time.sleep(3)

        remove_btn = driver.find_element(By.CLASS_NAME, "btn-danger")
        remove_btn.click()
        print("Задача удалена")
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при удалении задачи: {e}")
        driver.save_screenshot("remove_task_error.png")
        raise


def main():
    driver = None
    try:
        driver = create_driver()
        login(driver)
        open_tasks_section(driver)
        filter_tasks(driver)
        task_selection_and_mass_actions(driver)
        create_new_task(driver)
        remove_task(driver)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()