import base64
import os
import re
from contextlib import nullcontext

import requests
import cv2
import time
from io import BytesIO
from PIL import Image
from selenium.webdriver.common.by import By

captcha_url="https://plus.sjtu.edu.cn/captcha-solver/"

def base64_to_image(base64_str):
    base64_data=re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data=base64.b64decode(base64_data)
    image_data=BytesIO(byte_data)
    image=Image.open(image_data)
    return image

def get_captcha(driver):
    js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
         "let img = document.getElementsByTagName('img')[3]; /*找到图片*/ " \
         "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
         "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
         "let base64String = c.toDataURL();return base64String;"
    base64_str = driver.execute_script(js)
    img = base64_to_image(base64_str)
    return img

def captcha_recognize():
    result=requests.post(captcha_url, files={"image": open('captcha.jpg', 'rb')}).json()['result']
    return result

def captcha(driver):
    get_captcha(driver).save("captcha.png")
    img_data=cv2.imread("captcha.png")
    gray=cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),0)
    binary=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,2)
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    morph=cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel)
    cv2.imwrite('captcha.jpg',morph)
    result=captcha_recognize()
    os.remove("captcha.png")
    os.remove("captcha.jpg")
    return result

def login(driver):
    driver.get("https://my.sjtu.edu.cn/")
    if driver.current_url == "https://my.sjtu.edu.cn/ui/task":
        return True
    driver.find_element(By.ID, 'input-login-user').send_keys('T.resol')
    driver.find_element(By.ID, 'input-login-pass').send_keys('cuffyh-0wygwA-xipren')
    driver.find_element(By.ID, 'input-login-captcha').send_keys(captcha(driver))
    time.sleep(1)
    driver.find_element(By.ID, 'submit-password-button').click()
    time.sleep(1)
    if driver.current_url == "https://my.sjtu.edu.cn/ui/task":
        return True
    return False

def get_session_id(driver):
    if driver.get_cookie('JSESSIONID'):
        return driver.get_cookie('JSESSIONID')['value']
    return None

def logout(driver):
    driver.get("https://my.sjtu.edu.cn/")
    if driver.current_url != "https://my.sjtu.edu.cn/ui/task":
        return True
    driver.execute_cdp_cmd("Network.clearBrowserCookies", {
        "name": 'JSESSIONID'
    })
    driver.get("https://my.sjtu.edu.cn/")
    if driver.current_url != "https://my.sjtu.edu.cn/ui/task":
        return True
    return False