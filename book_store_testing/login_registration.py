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

def register_user(driver, login_user_func):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        my_account_link = driver.find_element(By.LINK_TEXT, "My Account")
        my_account_link.click()
        time.sleep(3)

        email_input = driver.find_element(By.ID, "reg_email")
        email = "testuser@example.com"
        email_input.send_keys(email)

        password_input = driver.find_element(By.ID, "reg_password")
        password = "StrongPassword123!"
        password_input.send_keys(password)

        register_button = driver.find_element(By.NAME, "register")
        register_button.click()
        time.sleep(3)

        register_error = driver.find_element(By.CLASS_NAME, "woocommerce-error")

        if register_error.is_displayed():
            print("[{}] Такой пользователь уже существует. Пожалуйста, залогиньтесь!".format(time.strftime('%H:%M:%S')))
            login_user_func(driver, email, password)
        else:
            print("[{}] Пользователь зарегистрирован".format(time.strftime('%H:%M:%S')))

        logout_link = driver.find_element(By.LINK_TEXT, "Logout")
        logout_link.click()
        time.sleep(3)

        print("[{}] Выход выполнен".format(time.strftime('%H:%M:%S')))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def login_user(driver, email, password):
    driver.implicitly_wait(10)
    try:
        email_input = driver.find_element(By.ID, "username")
        email_input.send_keys(email)

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        logout_link = driver.find_element(By.LINK_TEXT, "Logout")
        if logout_link.is_displayed():
            print("[{}] Логин выполнен успешно, элемент 'Logout' найден".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: элемент 'Logout' не найден".format(time.strftime('%H:%M:%S')))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def main():
    driver = None
    try:
        driver = create_driver()
        register_user(driver, login_user_func=login_user)
        email = "testuser@example.com"
        password = "StrongPassword123!"
        login_user(driver, email, password)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Критическая ошибка: {e}")
    finally:
        if driver:
            driver.quit()
            print(f"[{time.strftime('%H:%M:%S')}] Драйвер закрыт")
if __name__ == "__main__":
    main()