import requests
from selenium.webdriver import ActionChains, Keys
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
import jAccount
import academic
from selenium.webdriver.edge.options import Options

# driver_options=Options()
# driver_options.add_argument('--headless')

# driver=webdriver.Edge(options=driver_options)
driver=webdriver.Edge()
isLogin=False
while not isLogin:
    isLogin=jAccount.login(driver)
    time.sleep(1)
print(academic.get_score_list(0,0,driver))
input()
driver.close()