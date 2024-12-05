from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("C:/govno.html")
elementByLinkText = driver.find_element(By.LINK_TEXT, "Перейти к содержимому")
elementByPartialLinkText = driver.find_element(By.PARTIAL_LINK_TEXT, "Пере")
driver.quit()