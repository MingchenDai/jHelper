import time
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import json
import requests
import jAccount


def system_semester(semester):
    if semester == 1:
        return str(3)
    elif semester == 2:
        return str(12)
    elif semester == 3:
        return str(16)
    return None

# `year` should in syntax as '2024' and semester should be an integer in [1,3]
def get_selected_course_list(year, semester, driver):
    url="https://i.sjtu.edu.cn/xkcx/xkmdcx_cxXkmdcxIndex.html?doType=query&gnmkdm=N255010"
    request_parameter="&xnm="+str(year)+"&xqm="+system_semester(semester)
    request_parameter+=(("&kkxy_id=&kclbdm=&kcxzmc=&kch=&kklxdm=&kkzt=1&jxbmc=&jsxx=&kcgsdm=&xdbj=&fxbj=&cxbj=&zxbj="
                        "&sfzbh_kcflsj=&cxlx=&zyfx_id=&xklc=&_search=false&nd=")+str(int(time.time()))+
                        "&queryModel.showCount=100&queryModel.currentPage=1"
                        "&queryModel.sortName=xkbjmc%2Cxnmc%2Cxqmc%2Ckkxymc%2Ckch%2Cjxbmc%2Cxh+"
                        "&queryModel.sortOrder=asc&time=6")
    url+=request_parameter
    driver.get(url)
    driver.find_element(By.ID,"authJwglxtLoginURL").click()
    time.sleep(1)
    selected_course_list=json.loads(driver.find_element(By.TAG_NAME,"pre").text)['items']
    selected_course_list.sort(key=lambda course: course['jxbmc'])
    return selected_course_list

def get_ongoing_course_list(year,semester,driver):
    url = "https://i.sjtu.edu.cn/design/funcData_cxFuncDataList.html?func_widget_guid=8B04B7BBB49C4455E0530200A8C06482&gnmkdm=N2199113"
    request_parameter = "&xnm="+str(year)+"&xqm="+system_semester(semester)+"&queryModel.showCount=5000"
    url += request_parameter
    driver.get("https://i.sjtu.edu.cn/design/viewFunc_cxDesignFuncPageIndex.html?gnmkdm=N2199113&layout=default")
    time.sleep(1)
    driver.find_element(By.ID, "authJwglxtLoginURL").click()
    time.sleep(1)
    driver.get(url)
    selected_course_list = json.loads(driver.find_element(By.TAG_NAME, "pre").text)['items']
    selected_course_list.sort(key=lambda course: course['jxbmc'])
    return selected_course_list

# driver=webdriver.Edge()
# jAccount.login(driver)
#
# dataSource_consist = "https://i.sjtu.edu.cn/jxjcgl/jxjcwh_cxJxjdcxdcIndex.html?doType=query&gnmkdm=N155325"
# dataSource_detail = "https://i.sjtu.edu.cn/design/funcData_cxFuncDataList.html?func_widget_guid=8B04B7BBB49C4455E0530200A8C06482&gnmkdm=N2199113&xnm=2025&xqm=3&_search=false&nd="+str(int(time.time()*1000))+"&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=asc"
#
# metaData_head = {
#     "Accept": "application/json, text/javascript, */*; q=0.01",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
#     "Connection": "keep-alive",
#     "Cache-Control": "max-age=0",
#     "Cookie": "_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;"
#               "_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;"
#               "_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;"
#               "_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;"
#               "_ga=GA1.3.1152377759.1729079753;"
#               "_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;"
#               "i.sjtu.edu.cn=22632.57725.21071.0000;"
#               "JSESSIONID="+jAccount.get_session_id(driver),
#     "Host": "i.sjtu.edu.cn",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
#     "X-Requested-With": "XMLHttpRequest",
#     "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "Windows"
# }
# print(metaData_head["Cookie"])
# print(dataSource_detail)
# res=requests.get(dataSource_detail, headers=metaData_head)
# time.sleep(10)
# print(res.text)
# print(res.status_code)
# course_raw_detailed = json.loads(requests.get(dataSource_detail, headers=metaData_head).text)['items']
# course_raw_detailed.sort(key=lambda x: x['jxbmc'])
# course_detailed = []
# for item in course_raw_detailed:
#     # What's the fuck.
#     # | kcdm            | jxbmc                   | nj             | kcmc | jsxx                      | kcap                | xf     | skyy     | kkbm
#     # | Code for course | Code for teaching class | Code for grade | Name | Information of Teacher(s) | Course Arrangements | Points | Language | Academy
#     course_detailed.append(
#         [item['kcdm'], item['jxbmc'], item['nj'], item['kcmc'], item['jsxx'], item['kcap'], float(item['xf']),
#          item['skyy']])
#
# for course in course_detailed:
#     print(course)

def exams():
    head={
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "185",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": "_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;"
                  "_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;"
                  "_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;"
                  "_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;"
                  "_ga=GA1.3.1152377759.1729079753;"
                  "_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;"
                  "i.sjtu.edu.cn=22632.57526.21071.0000;"
                  "JSESSIONID="+"89CA06DC2B7344C72EBBFCEEAA742BD1",
        "Host": "i.sjtu.edu.cn",
        "Origin": "https://i.sjtu.edu.cn",
        "Referer": "https://i.sjtu.edu.cn/kwgl/kscx_cxXsksxxIndex.html?gnmkdm=N358105&layout=default",
        "Sec-Fetch-Dest": 'empty',
        "Sec-Fetch-Mode": 'cors',
        "Sec-Fetch-Site": 'same-origin',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        "X-Requested-With": 'XMLHttpRequest',
        "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }
    res=requests.post("https://i.sjtu.edu.cn/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105&xnm=2024&xqm=12",headers=head)
    print(res.status_code)
    print(res.text)

exams()