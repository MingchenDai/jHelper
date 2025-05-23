import requests
from selenium.webdriver import ActionChains, Keys
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
import jAccount
import Academic
from selenium.webdriver.edge.options import Options

# driver_options=Options()
# driver_options.add_argument('--headless')
# driver=webdriver.Edge()
# driver=webdriver.Firefox(options=driver_options)
# isLogin=False
# while not isLogin:
#     print("login")
#     isLogin=jAccount.login(driver)
#     time.sleep(1)
# course_list=Academic.get_complete_course_list(2025,1,driver)
# with open("list.txt","w",encoding='UTF-8')as f:
#     f.write(str(course_list))

print()
print("OK")
# driver.close()