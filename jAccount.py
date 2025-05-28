import base64
import os
import re
import requests
import cv2
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

import Files

captcha_url = "https://plus.sjtu.edu.cn/captcha-solver/"
jAccount = Files.read_config("jAccount", "jAccount")
password = Files.read_config("jAccount", "Password")


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    return Image.open(BytesIO(byte_data))


def get_captcha(driver) -> Image.Image:
    js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
         "let img = document.getElementsByTagName('img')[3]; /*找到图片*/ " \
         "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
         "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
         "let base64String = c.toDataURL();return base64String;"
    base64_str = driver.execute_script(js)
    return base64_to_image(base64_str)


def captcha_recognize() -> str:
    try:
        result = requests.post(captcha_url, files={"image": open('captcha.jpg', 'rb')}).json()['result']
        return result
    except Exception as e:
        raise RuntimeError(Files.exception_throw_out()) from e


def captcha(driver) -> str:
    get_captcha(driver).save("captcha.png")
    img_data = cv2.imread("captcha.png")
    gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    binary = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cv2.imwrite('captcha.jpg', morph)
    result = captcha_recognize()
    os.remove("captcha.png")
    os.remove("captcha.jpg")
    return result


def login(driver) -> bool:
    driver.get("https://i.sjtu.edu.cn/")
    time.sleep(1)

    try:
        driver.find_element(By.ID, "authJwglxtLoginURL").click()
    except Exception as e:
        raise RuntimeError(Files.exception_throw_out()) from e

    if "jaccount" not in driver.current_url:
        return True
    driver.find_element(By.ID, 'input-login-user').send_keys(jAccount)
    driver.find_element(By.ID, 'input-login-pass').send_keys(password)
    driver.find_element(By.ID, 'input-login-captcha').send_keys(captcha(driver))
    time.sleep(1)
    driver.find_element(By.ID, 'submit-password-button').click()
    time.sleep(1)
    return "jAccount" not in driver.current_url


def get_session_id(driver) -> str:
    cookie = driver.get_cookie('JSESSIONID')
    return cookie['value'] if cookie else None


def logout(driver) -> bool:
    driver.get("https://my.sjtu.edu.cn/")
    if driver.current_url != "https://my.sjtu.edu.cn/ui/task":
        return True
    try:
        driver.execute_cdp_cmd("Network.clearBrowserCookies", {"name": 'JSESSIONID'})
    except Exception as e:
        raise RuntimeError(Files.exception_throw_out()) from e
    driver.get("https://my.sjtu.edu.cn/")
    return True if 'jaccount' not in driver.current_url else False


def is_login(driver: 'webdriver' = None) -> bool:
    driver.get("https://my.sjtu.edu.cn/")
    return "jaccount" not in driver.current_url
