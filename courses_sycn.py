import base64
import os
import time
import numpy as np
import cv2
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_captcha(jAccountWebdriver):
    script="""
    var img = arguments[0];
    var canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    return canvas.toDataURL('image/png');
    """
    img_data=base64.b64decode(jAccountWebdriver.execute_script(script,jAccountWebdriver.find_element(By.ID,"captcha-img")).split(",",1)[1])
    img=cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
    thresh=cv2.adaptiveThreshold(cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),(5,5),0),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imwrite('captcha.jpg',thresh)
    captcha_text=requests.post("https://plus.sjtu.edu.cn/captcha-solver/",files={"image": open('captcha.jpg', 'rb')}).json()['result']
    os.remove('captcha.jpg')
    return captcha_text

def login(Webdriver):
    Webdriver.get("https://my.sjtu.edu.cn/")
    time.sleep(3)
    Webdriver.find_element(By.ID,'input-login-user').send_keys("jAccount")
    Webdriver.find_element(By.ID,'input-login-pass').send_keys("Password")
    Webdriver.find_element(By.ID,'input-login-captcha').send_keys(get_captcha(Webdriver))
    Webdriver.find_element(By.ID,'submit-password-button').click()
    time.sleep(3)
    if Webdriver.current_url=="https://mt.sjtu.edu.cn/ui/task":
        return True
    else:
        return False
# http://180.76.151.202/oauth/jacAuth.mooc