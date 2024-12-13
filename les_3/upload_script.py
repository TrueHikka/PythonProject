import random
import string
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
    driver.implicitly_wait(5)

    return driver

def filling_fields(driver, generated_password):
    try:
        driver.get("https://demo.automationtesting.in/Register.html")
        time.sleep(3)

        input_first_name = driver.find_element(By.XPATH, "//input[@placeholder='First Name']")
        input_first_name.click()
        input_first_name.send_keys("John")
        print(input_first_name.get_attribute('value'))

        input_last_name = driver.find_element(By.XPATH, "//input[@placeholder='Last Name']")
        input_last_name.click()
        input_last_name.send_keys("Doe")
        print(input_last_name.get_attribute('value'))

        time.sleep(3)

        input_email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        input_email.click()
        input_email.send_keys("5rY7t@example.com")
        print(input_email.get_attribute('value'))
        time.sleep(3)

        input_phone = driver.find_element(By.CSS_SELECTOR, "input[type='tel']")
        input_phone.click()
        input_phone.send_keys("9522673526")
        print(input_phone.get_attribute('value'))
        time.sleep(3)

        gender_input = driver.find_element(By.CSS_SELECTOR, ".form-group:nth-child(5) input[value='Male']")
        gender_input.click()
        print(gender_input.get_attribute('value'))
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        first_password = driver.find_element(By.ID, "firstpassword")
        first_password.click()
        first_password.send_keys(generated_password)
        print(first_password.get_attribute('value'))

        second_password = driver.find_element(By.ID, "secondpassword")
        second_password.click()
        second_password.send_keys(generated_password)
        print(second_password.get_attribute('value'))

        date_of_birth = driver.find_element(By.XPATH, "//select[@placeholder='Year']")
        select = Select(date_of_birth)
        select.select_by_value("1990")
        print(date_of_birth.get_attribute('value'))

        date_of_birth = driver.find_element(By.XPATH, "//select[@placeholder='Month']")
        select = Select(date_of_birth)
        select.select_by_value("January")
        print(date_of_birth.get_attribute('value'))

        date_of_birth = driver.find_element(By.XPATH, "//select[@placeholder='Day']")
        select = Select(date_of_birth)
        select.select_by_value("1")
        print(date_of_birth.get_attribute('value'))

        # Избегаем необходимость экранировать обратные слэши
        file = r'C:\Users\Lenovo\OneDrive\Рабочий стол\wallpaper\aesthetic-anime-character-gaming.jpg'
        upload_image = driver.find_element(By.ID, "imagesrc")
        upload_image.send_keys(file)
        time.sleep(3)

        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(3)

        submit_btn = driver.find_element(By.ID, "submitbtn")
        submit_btn.click()
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при выполнении задания: {e}")
        driver.save_screenshot("task_error.png")
        raise

def generate_complex_password(length, random_char_func):
    # Если length пароля меньше 6, то устанавливаем длину пароля в 6
    length = max(length, 6)

    # Создание списка, состоящего из 3 символов
    password = [
        # Выбор случайной строчной буквы
        random_char_func(string.ascii_lowercase),
        # Выбор случайной прописной буквы
        random_char_func(string.ascii_uppercase),
        # Выбор случайного числа
        random_char_func(string.digits)
    ]

    # Создаем строку, которая содержит все буквы (как строчные, так и прописные) и цифры
    all_chars = string.ascii_letters + string.digits

    # Расширение пароля
    password.extend(
        # Выбираем случайные символы в количестве входящей длины (8 символов) - 3 (строчные буквы, прописные буквы, цифры)
        # Получаем 5 случайных символов, которые расширят пароль до 8 символов
        random_char_func(all_chars)
        for _ in range(length - len(password))
    )

    # Перемешивание пароля
    random.shuffle(password)

    # Перевод в строку
    return "".join(password)

def main():
    def get_random_char(char_set):
        # Преобразует строку символов в список и выбирает случайный элемент
        return random.choice(list(char_set))

    driver = None
    try:
        driver = create_driver()
        generated_password = generate_complex_password(length=8, random_char_func=get_random_char)
        filling_fields(driver, generated_password)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()