import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://opensource-demo.orangehrmlive.com/")
time.sleep(3)

login = driver.find_element(By.NAME,"username")
login.send_keys("Admin")

password = driver.find_element(By.NAME,"password")
password.send_keys("admin123")

login_btn = driver.find_element(By.CLASS_NAME, "oxd-button")
login_btn.click()
time.sleep(3)

driver.quit()