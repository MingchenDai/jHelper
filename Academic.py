import requests
import jAccount
from typing import Optional, Dict, List, Any
import seleniumwire.webdriver as webdriver

SEMESTER_MAP = {
    1: "3",
    2: "12",
    3: "16"
}


def system_semester(semester: int) -> Optional[str]:
    return SEMESTER_MAP.get(semester)


def get_current_information() -> tuple[int, int, int]:
    request_url = "https://ids.sjtu.edu.cn/course/findCurSemester"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        data = response.json()["data"]
        week = data["week"]
        semester = data["semester"]
        year = int((int(str(data["year"]).replace("-", "")) - 1) / 10001)
        return week, semester, year
    except (requests.RequestException, KeyError, ValueError) as e:
        raise RuntimeError("Fail at function Academic.get_current_information") from e


def build_headers(cookie: str, referer: str) -> dict:
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "321",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        'Cookie': cookie,
        "Host": "i.sjtu.edu.cn",
        "Origin": "https://i.sjtu.edu.cn",
        "Referer": referer,
        "Sec-Fetch-Dest": 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
    }


def get_list(year: int, semester: int, request_url: str, default_request_parameter: str, cookie: str, referer: str,
             driver: webdriver, session_id: Optional[str]) -> List[Dict[str, Any]]:
    if session_id:
        cookie += session_id
    else:
        cookie += jAccount.get_session_id(driver)
    request_parameter = f"&xnm={str(year)}" if year else "&xnm="
    request_parameter += f"&xqm={system_semester(semester)}" if semester else "&xqm="
    request_parameter += default_request_parameter
    head = build_headers(cookie, referer)
    try:
        response = requests.post(url=request_url + request_parameter, headers=head)
        response.raise_for_status()
        return response.json().get("items", [])
    except(requests.RequestException, ValueError) as e:
        raise RuntimeError("Fail at function Academic.get_list") from e


# `year` should in syntax as '2024' and semester should be an integer in [1,3]
def get_selected_course_list(year:'int'=0, semester:'int'=0, driver:'webdriver'=None, session_id:'str'=None):
    referer = 'https://i.sjtu.edu.cn/kwgl/kscx_cxXsksxxIndex.html?gnmkdm=N358105&layout=default'
    request_url = "https://i.sjtu.edu.cn/xkcx/xkmdcx_cxXkmdcxIndex.html?doType=query&gnmkdm=N255010"
    request_parameter = "&kkxy_id=&kclbdm=&kcxzmc=&kch=&kklxdm=&kkzt=1&jxbmc=&jsxx=&kcgsdm=&xdbj=&fxbj=&cxbj=&zxbj=&sfzbh_kcflsj=&cxlx=&zyfx_id=&xklc=&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=xkbjmc%2Cxnmc%2Cxqmc%2Ckkxymc%2Ckch%2Cjxbmc%2Cxh+&queryModel.sortOrder=asc"
    cookie = ('_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
              '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
              '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
              '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
              '_ga=GA1.3.1152377759.1729079753;'
              '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
              'i.sjtu.edu.cn=22632.58179.21071.0000;'
              'JSESSIONID=')
    return get_list(year,semester,request_url,request_parameter,cookie,referer,driver,session_id)


def get_exam_list(year:'int'=0, semester:'int'=0, driver:'webdriver'=None, session_id:'str'=None):
    referer = 'https://i.sjtu.edu.cn/xkcx/xkmdcx_cxXkmdcxIndex.html?gnmkdm=N255010&layout=default'
    request_url = 'https://i.sjtu.edu.cn/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105'
    request_parameter = '&ksmcdmb_id=&kch=&kc=&ksrq=&kkbm_id=&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=asc'
    cookie = ('_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
              '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
              '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
              '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
              '_ga=GA1.3.1152377759.1729079753;'
              '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
              'i.sjtu.edu.cn=22632.57526.21071.0000;'
              'JSESSIONID=')
    return get_list(year, semester, request_url, request_parameter, cookie, referer, driver, session_id)


def get_score_list(year:'int'=0, semester:'int'=0, driver:'webdriver'=None, session_id:'str'=None):
    referer='https://i.sjtu.edu.cn/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default'
    request_url = 'https://i.sjtu.edu.cn/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005'
    request_parameter = '&kcbj=&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=asc'
    cookie=('_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
            '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
            '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
            '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
            '_ga=GA1.3.1152377759.1729079753;'
            '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
            'i.sjtu.edu.cn=22632.57526.21071.0000;'
            'JSESSIONID=')
    return get_list(year, semester, request_url, request_parameter, cookie, referer, driver, session_id)


def get_ongoing_course_list(year:'int'=0, semester:'int'=0, driver:'webdriver'=None, session_id:'str'=None):
    referer='https://i.sjtu.edu.cn/design/viewFunc_cxDesignFuncPageIndex.html?gnmkdm=N2199113&layout=default'
    request_url = 'https://i.sjtu.edu.cn/design/funcData_cxFuncDataList.html?func_widget_guid=8B04B7BBB49C4455E0530200A8C06482&gnmkdm=N2199113'
    request_parameter = '&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=asc'
    cookie=('_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
            '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
            '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
            '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
            '_ga=GA1.3.1152377759.1729079753;'
            '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
            'i.sjtu.edu.cn=22632.58179.21071.0000;'
            'JSESSIONID=')
    return get_list(year, semester, request_url, request_parameter, cookie, referer, driver, session_id)


def get_detailed_course_list(year:'int'=0, semester:'int'=0, driver:'webdriver'=None, session_id:'str'=None):
    referer='https://i.sjtu.edu.cn/jxjcgl/jxjcwh_cxJxjdcxdcIndex.html?gnmkdm=N155325&layout=default'
    request_url = 'https://i.sjtu.edu.cn/jxjcgl/jxjcwh_cxJxjdcxdcIndex.html?doType=query&gnmkdm=N155325'
    request_parameter = '&kkbm_id=&kch=&kcmc=&jsxm=&xsdm=&zc=&rlzt=&xqh_id=&njdm_id=&zyh_id=&bjmc=&jxbmc=&cdmc=&kcxzdm=&_search=false&queryModel.showCount=5000&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=asc'
    cookie=('_ga_5G709VBQWD=GS1.3.1729079753.1.1.1729079788.0.0.0;'
            '_ga_ZLV69XZE3V=GS1.1.1733391784.1.0.1733391787.0.0.0;'
            '_ga_VGHWLGCC9B=GS1.1.1739709830.3.1.1739709850.0.0.0;'
            '_ga_S9DWX8R79S=GS1.1.1744951884.1.0.1744951888.0.0.0;'
            '_ga=GA1.3.1152377759.1729079753;'
            '_ga_6VSNHLPM65=GS1.3.1745074767.14.0.1745074767.0.0.0;'
            'i.sjtu.edu.cn=22632.58179.21071.0000;'
            'JSESSIONID=')
    return get_list(year, semester, request_url, request_parameter, cookie, referer, driver, session_id)


def get_complete_course_list(year:'int'=0, semester:'int'=0, driver:'webdriver'=None, session_id:'str'=None):
    ongoing_course_list = get_ongoing_course_list(year, semester, driver, session_id)
    ongoing_course_list.sort(key=lambda course:course['jxbmc'])
    detailed_course_list = get_detailed_course_list(year, semester, driver, session_id)
    ongoing_course_list.sort(key=lambda course: course['jxbmc'])
