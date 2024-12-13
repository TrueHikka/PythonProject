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

def transition(driver):
    try:
        driver.get("https://demo.automationtesting.in/WebTable.html")
        time.sleep(3)

        switch_to_link = driver.find_element(By.LINK_TEXT, "SwitchTo")
        switch_to_link.click()
        time.sleep(3)

        alerts_link = driver.find_element(By.LINK_TEXT, "Alerts")
        alerts_link.click()
        time.sleep(3)

        bnt_danger = driver.find_element(By.CLASS_NAME, "btn-danger")
        bnt_danger.click()
        time.sleep(3)

        alert_script = driver.switch_to.alert
        alert_text = alert_script.text
        print(alert_text)
        alert_script.accept()

        if alert_text == "I am an alert box!":
            print("Текст соответствует содержимому alert box")
        else:
            print("Текст не соответствует содержимому alert box")

        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при выполнении задания: {e}")
        driver.save_screenshot("task_error.png")
        raise

def window(driver):
    try:
        current_url = driver.current_url
        print(current_url)
        time.sleep(3)

        driver.execute_script("window.open();")
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        driver.get(current_url)
        time.sleep(3)

        confirm_btn_link = driver.find_element(By.LINK_TEXT, "Alert with OK & Cancel")
        confirm_btn_link.click()
        time.sleep(3)

        btn_primary_confirm_window_link = driver.find_element(By.CLASS_NAME, "btn-primary")
        btn_primary_confirm_window_link.click()
        time.sleep(3)

        alert_script = driver.switch_to.alert
        alert_script.dismiss()
        time.sleep(3)

        driver.execute_script("window.open();")
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        driver.get(current_url)
        time.sleep(3)

        prompt_btn_link = driver.find_element(By.LINK_TEXT, "Alert with Textbox")
        prompt_btn_link.click()
        time.sleep(3)

        btn_info_prompt_window_link = driver.find_element(By.CLASS_NAME, "btn-info")
        btn_info_prompt_window_link.click()
        time.sleep(3)

        alert_script = driver.switch_to.alert
        alert_script.send_keys("Ура! Задание выполнено!")
        alert_script.accept()
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при выполнении задания: {e}")
        driver.save_screenshot("task_error.png")
        raise
def main():
    driver = None
    try:
        driver = create_driver()
        transition(driver)
        window(driver)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()