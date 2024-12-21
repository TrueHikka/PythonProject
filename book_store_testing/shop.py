import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
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

def check_product_page_display(driver):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        shop_link = driver.find_element(By.LINK_TEXT, "Shop")
        shop_link.click()
        print("[{}] Нажата вкладка 'Shop'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        html_book_link = driver.find_element(By.CLASS_NAME, "post-181")
        html_book_link.get_attribute("href")
        html_book_link.click()
        print("[{}] Открыта книга 'HTML5 Forms'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        book_title = driver.find_element(By.CSS_SELECTOR, "div h1")
        if book_title.text == "HTML5 Forms":
            print("[{}] Заголовок книги: 'HTML5 Forms'".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: заголовок книги не соответствует ожидаемому".format(time.strftime('%H:%M:%S')))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def check_html_category(driver):
    driver.implicitly_wait(10)

    try:
        driver.get("https://practice.automationtesting.in/")

        shop_link = driver.find_element(By.LINK_TEXT, "Shop")
        shop_link.click()

        time.sleep(3)

        html_category_link = driver.find_element(By.LINK_TEXT, "HTML")
        html_category_link.click()

        time.sleep(3)

        products = driver.find_elements(By.CSS_SELECTOR, ".products li")
        if len(products) == 3:
            print("[{}] Отображается три товара в категории 'HTML'".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: количество товаров в категории 'HTML' не равно трем".format(time.strftime('%H:%M:%S')))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def check_sorting(driver, login_user):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        login_user()

        time.sleep(3)

        shop_link = driver.find_element(By.LINK_TEXT, "Shop")
        shop_link.click()
        print("[{}] Нажата вкладка 'Shop'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        driver.execute_script("window.scrollBy(0, 500);")

        time.sleep(3)

        default_sorting_select = Select(driver.find_element(By.CSS_SELECTOR, ".orderby"))
        default_option = default_sorting_select.first_selected_option
        if default_option.get_attribute("value") == "menu_order":
            print("[{}] Вариант сортировки по умолчанию выбран".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: вариант сортировки по умолчанию не выбран".format(time.strftime('%H:%M:%S')))

        sorting_select = Select(driver.find_element(By.CSS_SELECTOR, ".orderby"))
        sorting_select.select_by_value("price-desc")
        print("[{}] Товары отсортированы по цене от большей к меньшей".format(time.strftime('%H:%M:%S')))

        driver.execute_script("window.scrollBy(0, 500);")

        time.sleep(3)

        sorting_select = Select(driver.find_element(By.CSS_SELECTOR, ".orderby"))

        selected_option = sorting_select.first_selected_option
        if selected_option.get_attribute("value") == "price-desc":
            print("[{}] Вариант сортировки по цене от большей к меньшей выбран".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: вариант сортировки по цене от большей к меньшей не выбран".format(time.strftime('%H:%M:%S')))

        time.sleep(3)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def check_discount_and_preview(driver, login_user):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        login_user()

        shop_link = driver.find_element(By.LINK_TEXT, "Shop")
        shop_link.click()
        print("[{}] Нажата вкладка 'Shop'".format(time.strftime('%H:%M:%S')))

        book_link = driver.find_element(By.CLASS_NAME, "post-169")
        book_link.get_attribute("href")
        book_link.click()
        print("[{}] Открыта книга 'Android Quick Start Guide'".format(time.strftime('%H:%M:%S')))

        old_price = driver.find_element(By.CSS_SELECTOR, ".price del")
        if old_price.text == "₹600.00":
            print("[{}] Содержимое старой цены = '₹600.00'".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: содержимое старой цены не равно '₹600.00'".format(time.strftime('%H:%M:%S')))

        new_price = driver.find_element(By.CSS_SELECTOR, ".price ins")
        if new_price.text == "₹450.00":
            print("[{}] Содержимое новой цены = '₹450.00'".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: содержимое новой цены не равно '₹450.00'".format(time.strftime('%H:%M:%S')))

        book_image = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".images img"))
        )
        book_image.click()
        print("[{}] Нажата обложка книги".format(time.strftime('%H:%M:%S')))

        time.sleep(2)
        preview_window = driver.find_element(By.CSS_SELECTOR, ".pp_pic_holder img")
        if preview_window.is_displayed():
            print("[{}] Окно предпросмотра картинки открыто".format(time.strftime('%H:%M:%S')))
        else:
            print("[{}] Ошибка: окно предпросмотра картинки не открыто".format(time.strftime('%H:%M:%S')))

        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".pp_close"))
        )
        close_button.click()
        print("[{}] Предпросмотр закрыт".format(time.strftime('%H:%M:%S')))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def wait_for_element_visibility(driver, locator, timeout=10, condition=EC.visibility_of_element_located):
    try:
        element = WebDriverWait(driver, timeout).until(
            condition(locator)
        )
        return element
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {str(e)}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def check_add_to_cart(driver):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        shop_link = driver.find_element(By.LINK_TEXT, "Shop")
        shop_link.click()
        print("[{}] Нажата вкладка 'Shop'".format(time.strftime('%H:%M:%S')))

        html5_webapp_book = driver.find_element(By.CLASS_NAME, "post-182")
        add_to_chart_btn_link = html5_webapp_book.find_element(By.CLASS_NAME, "add_to_cart_button")
        add_to_chart_btn_link.click()
        print("[{}] Книга 'HTML5 WebApp Development' добавлена в корзину".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        cart_contents = driver.find_element(By.CSS_SELECTOR, ".cartcontents")
        cart_price = driver.find_element(By.CSS_SELECTOR, ".wpmenucart-contents .amount")
        assert cart_contents.text == "1 Item" and cart_price.text == "₹180.00"
        print("[{}] Проверка количества товаров в корзине и Subtotal стоимости пройдена".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        view_cart_link = driver.find_element(By.CSS_SELECTOR, ".wc-forward")
        view_cart_link.click()
        print("[{}] Переход в корзину успешен".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        time.sleep(3)
        wait_for_element_visibility(driver, (By.CSS_SELECTOR, ".cart-subtotal .amount"))
        print("[{}] Проверка Subtotal отображаемой стоимости пройдена".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        wait_for_element_visibility(driver, (By.CSS_SELECTOR, ".order-total .amount"))
        print("[{}] Проверка Total отображаемой стоимости пройдена".format(time.strftime('%H:%M:%S')))
        time.sleep(3)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def working_with_the_shopping_cart(driver):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        shop_link = driver.find_element(By.LINK_TEXT, "Shop")
        shop_link.click()
        print("[{}] Нажата вкладка 'Shop'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        html5_webapp_book = driver.find_element(By.CLASS_NAME, "post-182")
        add_to_chart_btn_link = html5_webapp_book.find_element(By.CLASS_NAME, "add_to_cart_button")
        add_to_chart_btn_link.click()
        print("[{}] Книга 'HTML5 WebApp Development' добавлена в корзину".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        js_data_structures_book = driver.find_element(By.CLASS_NAME, "post-180")
        add_to_chart_btn_link = js_data_structures_book.find_element(By.CLASS_NAME, "add_to_cart_button")
        add_to_chart_btn_link.click()
        print("[{}] Книга 'JS Data Structures and Algorithm' добавлена в корзину".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        view_cart_link = driver.find_element(By.CSS_SELECTOR, ".wc-forward")
        view_cart_link.click()
        print("[{}] Переход в корзину успешен".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        first_book_remove_link = driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(1) .product-remove a")
        first_book_remove_link.click()
        print("[{}] Первая книга удалена из корзины".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        undo_link = driver.find_element(By.LINK_TEXT, "Undo?")
        undo_link.click()
        print("[{}] Нажата кнопка 'Undo'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        quantity_input = driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(1) .input-text")
        quantity_input.clear()
        quantity_input.send_keys("3")
        print("[{}] Количество товара 'JS Data Structures and Algorithm' увеличено до 3".format(time.strftime('%H:%M:%S')))

        update_basket_button = driver.find_element(By.NAME, "update_cart")
        update_basket_button.click()
        print("[{}] Нажата кнопка 'UPDATE BASKET'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        quantity_value = driver.find_element(By.CSS_SELECTOR, ".cart_item:nth-child(1) .input-text").get_attribute("value")
        assert quantity_value == "3", "Количество товара 'JS Data Structures and Algorithm' не равно 3"
        print("[{}] Проверка количества товара 'JS Data Structures and Algorithm' пройдена".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        apply_coupon_button = driver.find_element(By.NAME, "apply_coupon")
        apply_coupon_button.click()
        print("[{}] Нажата кнопка 'APPLY COUPON'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        error_message = driver.find_element(By.CSS_SELECTOR, ".woocommerce-error").text
        assert error_message == "Please enter a coupon code.", "Сообщение об ошибке не соответствует ожидаемому"
        print("[{}] Проверка сообщения об ошибке пройдена".format(time.strftime('%H:%M:%S')))
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def check_purchase(driver):
    driver.implicitly_wait(10)
    try:
        driver.get("https://practice.automationtesting.in/")

        shop_link = driver.find_element(By.LINK_TEXT, "Shop")
        shop_link.click()
        print("[{}] Нажата вкладка 'Shop'".format(time.strftime('%H:%M:%S')))

        driver.execute_script("window.scrollBy(0, 300);")
        print("[{}] Проскроллено на 300 пикселей вниз".format(time.strftime('%H:%M:%S')))
        time.sleep(3)

        html5_webapp_book = driver.find_element(By.CLASS_NAME, "post-182")
        add_to_chart_btn_link = html5_webapp_book.find_element(By.CLASS_NAME, "add_to_cart_button")
        add_to_chart_btn_link.click()
        print("[{}] Книга 'HTML5 WebApp Development' добавлена в корзину".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        view_cart_link = driver.find_element(By.CSS_SELECTOR, ".wc-forward")
        view_cart_link.click()
        print("[{}] Переход в корзину успешен".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        proceed_to_checkout_button = driver.find_element(By.CSS_SELECTOR, ".checkout-button")
        proceed_to_checkout_button.click()
        print("[{}] Нажата кнопка 'PROCEED TO CHECKOUT'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        first_name_input = driver.find_element(By.ID, "billing_first_name")
        first_name_input.send_keys("John")
        print("[{}] Заполнено поле 'First Name'".format(time.strftime('%H:%M:%S')))

        last_name_input = driver.find_element(By.ID, "billing_last_name")
        last_name_input.send_keys("Doe")
        print("[{}] Заполнено поле 'Last Name'".format(time.strftime('%H:%M:%S')))

        email_input = driver.find_element(By.ID, "billing_email")
        email_input.clear()
        email_input.send_keys("V6xhM@example.com")
        print("[{}] Заполнено поле 'Email'".format(time.strftime('%H:%M:%S')))

        phone_input = driver.find_element(By.ID, "billing_phone")
        phone_input.send_keys("1234567890")
        print("[{}] Заполнено поле 'Phone'".format(time.strftime('%H:%M:%S')))

        country_dropdown = driver.find_element(By.ID, "select2-chosen-1")
        country_dropdown.click()
        time.sleep(2)

        country_search = driver.find_element(By.ID, "s2id_autogen1_search")
        country_search.send_keys("India")
        time.sleep(2)

        country_option = driver.find_element(By.CSS_SELECTOR, "#select2-results-1 li:nth-child(2)")
        country_option.click()
        print("[{}] Выбран вариант 'India' в поле 'Country'".format(time.strftime('%H:%M:%S')))
        time.sleep(2)

        city_input = driver.find_element(By.ID, "billing_city")
        city_input.send_keys("Bengaluru")
        print("[{}] Заполнено поле 'City'".format(time.strftime('%H:%M:%S')))

        address_input = driver.find_element(By.ID, "billing_address_1")
        address_input.send_keys("123 Main St")
        print("[{}] Заполнено поле 'Address'".format(time.strftime('%H:%M:%S')))

        state_link = driver.find_element(By.CSS_SELECTOR, ".state_select .select2-choice")
        state_link.click()

        state_search = driver.find_element(By.CSS_SELECTOR, ".select2-search #s2id_autogen2_search")
        state_search.send_keys("Karnataka")
        time.sleep(2)

        state_option = driver.find_element(By.CLASS_NAME, "select2-match")
        state_option.click()
        print("[{}] Выбран вариант 'Karnataka' в поле 'State'".format(time.strftime('%H:%M:%S')))

        postcode_input = driver.find_element(By.ID, "billing_postcode")
        postcode_input.send_keys("560001")
        print("[{}] Заполнено поле 'Postcode'".format(time.strftime('%H:%M:%S')))
        time.sleep(3)

        check_payments_radio = driver.find_element(By.ID, "payment_method_cheque")
        check_payments_radio.click()
        print("[{}] Выбран способ оплаты 'Check Payments'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        place_order_button = driver.find_element(By.ID, "place_order")
        place_order_button.click()
        print("[{}] Нажата кнопка 'PLACE ORDER'".format(time.strftime('%H:%M:%S')))

        time.sleep(3)

        thank_you_message = driver.find_element(By.CSS_SELECTOR, ".woocommerce-thankyou-order-received")
        assert thank_you_message.is_displayed(), "Сообщение 'Thank you. Your order has been received.' не отображается"
        print("[{}] Проверка сообщения 'Thank you. Your order has been received.' пройдена".format(time.strftime('%H:%M:%S')))

        payment_method_text = driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) td")
        assert payment_method_text.text == "Check Payments", "Payment Method не соответствует ожидаемому"
        print("[{}] Проверка Payment Method 'Check Payments' пройдена".format(time.strftime('%H:%M:%S')))

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
        driver.save_screenshot(f"test_error_{int(time.time())}.png")
        raise

def main():
    driver = None
    try:
        driver = create_driver()
        check_html_category(driver)
        check_product_page_display(driver)
        email = "testuser@example.com"
        password = "StrongPassword123!"
        def login_user():
            driver.implicitly_wait(10)
            try:
                driver.get("https://practice.automationtesting.in/")

                my_account_link = driver.find_element(By.LINK_TEXT, "My Account")
                my_account_link.click()
                time.sleep(3)

                email_input = driver.find_element(By.ID, "username")
                email_input.send_keys(email)

                password_input = driver.find_element(By.ID, "password")
                password_input.send_keys(password)

                login_button = driver.find_element(By.NAME, "login")
                login_button.click()
                time.sleep(3)

                print("[{}] Логин выполнен успешно".format(time.strftime('%H:%M:%S')))
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] Ошибка в тесте: {e}")
                driver.save_screenshot(f"test_error_{int(time.time())}.png")
                raise

        check_sorting(driver, login_user)
        check_discount_and_preview(driver, login_user)
        check_add_to_cart(driver)
        working_with_the_shopping_cart(driver)
        check_purchase(driver)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Критическая ошибка: {e}")
    finally:
        if driver:
            driver.quit()
            print(f"[{time.strftime('%H:%M:%S')}] Драйвер закрыт")
if __name__ == "__main__":
    main()