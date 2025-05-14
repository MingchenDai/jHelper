import requests
import jAccount


def get_request_head(driver):
    head = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;"
                  "_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;"
                  "_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;"
                  "_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;"
                  "_ga=GA1.3.1152377759.1729079753;"
                  "_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;"
                  "i.sjtu.edu.cn=22632.57526.21071.0000;"
                  "JSESSIONID=" + jAccount.get_session_id(driver) + ";",
        "Host": "i.sjtu.edu.cn",
        "Sec-Fetch-Dest": 'empty',
        "Sec-Fetch-Mode": 'cors',
        "Sec-Fetch-Site": 'same-origin',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        "X-Requested-With": 'XMLHttpRequest',
        "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
    }

    return head


def system_semester(semester):
    if semester == 1:
        return str(3)
    elif semester == 2:
        return str(12)
    elif semester == 3:
        return str(16)
    return None


def get_current_information():
    request_url = "https://ids.sjtu.edu.cn/course/findCurSemester"
    target_string = requests.get(request_url).json()["data"]
    week = str(target_string["week"])
    semester = int(target_string["sename"])
    year = int((int(str(target_string["year"]).replace("-", "")) - 1) / 10001)
    return year, semester, week


# `year` should in syntax as '2024' and semester should be an integer in [1,3]
def get_selected_course_list(year=get_current_information()[0], semester=get_current_information()[1], driver=None,
                             session_id=None):
    head = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "321",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        'Cookie': '_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
                  '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
                  '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
                  '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
                  '_ga=GA1.3.1152377759.1729079753;'
                  '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
                  'i.sjtu.edu.cn=22632.57526.21071.0000;'
                  'JSESSIONID=' + jAccount.get_session_id(driver),
        "Host": "i.sjtu.edu.cn",
        "Origin": "https://i.sjtu.edu.cn",
        "Referer": 'https://i.sjtu.edu.cn/xkcx/xkmdcx_cxXkmdcxIndex.html?gnmkdm=N255010&layout=default',
        "Sec-Fetch-Dest": 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
    }
    if session_id is None:
        head['Cookie'] += jAccount.get_session_id(driver)
    else:
        head['Cookie'] += session_id
    request_url = "https://i.sjtu.edu.cn/xkcx/xkmdcx_cxXkmdcxIndex.html?doType=query&gnmkdm=N255010"
    request_parameter = '&xnm='
    if year != 0:
        request_parameter += str(year)
    request_parameter += '&xqm='
    if semester != 0:
        request_parameter += system_semester(semester)
    request_parameter += "&kkxy_id=&kclbdm=&kcxzmc=&kch=&kklxdm=&kkzt=1&jxbmc=&jsxx=&kcgsdm=&xdbj=&fxbj=&cxbj=&zxbj=&sfzbh_kcflsj=&cxlx=&zyfx_id=&xklc=&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=xkbjmc%2Cxnmc%2Cxqmc%2Ckkxymc%2Ckch%2Cjxbmc%2Cxh+&queryModel.sortOrder=asc"
    selected_course_list = requests.post(url=request_url + request_parameter, headers=head).json()["items"]
    return selected_course_list


def get_exam_list(year=get_current_information()[0], semester=get_current_information()[1], driver=None,
                  session_id=None):
    head = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '185',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': '_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
                  '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
                  '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
                  '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
                  '_ga=GA1.3.1152377759.1729079753;'
                  '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
                  'i.sjtu.edu.cn=22632.57526.21071.0000;'
                  'JSESSIONID=',
        'Host': 'i.sjtu.edu.cn',
        'Origin': 'https://i.sjtu.edu.cn',
        'Referer': 'https://i.sjtu.edu.cn/kwgl/kscx_cxXsksxxIndex.html?gnmkdm=N358105&layout=default',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
    }
    if session_id is None:
        head['Cookie'] += jAccount.get_session_id(driver)
    else:
        head['Cookie'] += session_id
    request_url = 'https://i.sjtu.edu.cn/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105'
    request_parameter = '&xnm='
    if year != 0:
        request_parameter += str(year)
    request_parameter += '&xqm='
    if semester != 0:
        request_parameter += system_semester(semester)
    request_parameter += '&ksmcdmb_id=&kch=&kc=&ksrq=&kkbm_id=&_search=false&nd=1747225053795&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=asc&time=1'
    exam_list = requests.post(url=request_url + request_parameter, headers=head).json()["items"]
    return exam_list


def get_score_list(year=get_current_information()[0], semester=get_current_information()[1], driver=None,
                   session_id=None):
    head = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '155',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cookie': '_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
                  '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
                  '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
                  '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
                  '_ga=GA1.3.1152377759.1729079753;'
                  '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
                  'i.sjtu.edu.cn=22632.57526.21071.0000;'
                  'JSESSIONID=',
        'Host': 'i.sjtu.edu.cn',
        'Origin': 'https://i.sjtu.edu.cn',
        'Referer': 'https://i.sjtu.edu.cn/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    if session_id is None:
        head['Cookie'] += jAccount.get_session_id(driver)
    else:
        head['Cookie'] += session_id
    request_url='https://i.sjtu.edu.cn/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005'
    request_parameter = '&xnm='
    if year != 0:
        request_parameter += str(year)
    request_parameter += '&xqm='
    if semester != 0:
        request_parameter += system_semester(semester)
    request_parameter += '&kcbj=&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=asc'
    score_list = requests.post(url=request_url + request_parameter, headers=head).json()["items"]
    return score_list