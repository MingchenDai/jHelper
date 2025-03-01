import os
import time
import numpy as np
import cv2
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_captcha(jAccountWebdriver):
    img_url=jAccountWebdriver.find_element(By.ID,'captcha-img').get_attribute('src')
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "Referer": Webdriver.current_url,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "jaccount.sjtu.edu.cn",
        "Sec-Ch-Ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }
    img_data=requests.get(img_url,headers=header).content
    img=cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
    thresh=cv2.adaptiveThreshold(cv2.GaussianBlur(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),(5,5),0),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imwrite('captcha.jpg',thresh)
    captcha_text=requests.post("https://plus.sjtu.edu.cn/captcha-solver/",files={"image": open('captcha.jpg', 'rb')}).json()['result']
    print(captcha_text)
    return captcha_text

Webdriver=webdriver.Edge()
Webdriver.get('http://180.76.151.202/oauth/jacAuth.mooc')
Webdriver.find_element(By.ID,'input-login-user').send_keys("username")
time.sleep(1)
Webdriver.find_element(By.ID,'input-login-pass').send_keys("password")
time.sleep(1)
get_captcha(Webdriver)
Webdriver.find_element(By.ID,'input-login-captcha').send_keys(get_captcha(Webdriver))
time.sleep(1)
Webdriver.find_element(By.ID,'submit-password-button').click()
time.sleep(10)
Webdriver.quit()
# http://180.76.151.202/oauth/jacAuth.mooc