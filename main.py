import requests
from selenium.webdriver import ActionChains, Keys
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
import jAccount
import Academic
from selenium.webdriver.edge.options import Options

driver_options=Options()
driver_options.add_argument('--headless')
driver=webdriver.Edge(options=driver_options)
isLogin=False
while not isLogin:
    isLogin=jAccount.login(driver)
    time.sleep(1)
print(Academic.get_gpa(2024,2024,1,2,True,driver))
print("OK")
driver.close()