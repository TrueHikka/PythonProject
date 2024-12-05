import time

#! Импорт webdriver(набор команд для управления браузером)
from selenium import webdriver
from selenium.webdriver.common.by import By

#! Вызываем драйвер браузера. Должны увидеть новое окно браузера
driver = webdriver.Chrome()

time.sleep(5)

#! Открываем сайт по указанной ссылке
driver.get("https://www.google.com/")
time.sleep(5)

#! Метод позволяет найти нужный эл-нт на сайте
#textfield = driver.find_element("//textarea[@name='q']")
textfield = driver.find_element(By.NAME, "q")
#! Передаем в этот эл-т текст
textfield.send_keys("Selenium")
time.sleep(5)

#! Указываем путь к кнопке
#submit_button = driver.find_element("//div[@jsname='VlcLAe']//input[@class='gNO89b']")
submit_button = driver.find_element(By.NAME, "btnK")
#! Нажимаем на кнопку
submit_button.click()
time.sleep(5)

#! Закрываем браузер
driver.quit()