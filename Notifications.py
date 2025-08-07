from typing import Tuple, List, Dict
import requests
from bs4 import BeautifulSoup


def get_academic_news() -> Tuple[bool, List[Dict[str, str]]]:
    target_url = 'https://jwc.sjtu.edu.cn/xwtg/tztg.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(target_url, headers=headers)
    if response.status_code != requests.codes.ok:
        return False, []

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    news_list = soup.find_all('li', class_='clearfix')

    result = []
    for news in news_list:
        try:
            date_raw = news.find('div', class_='sj')
            day = date_raw.find('h2').text.strip()
            month_year = date_raw.find('p').text.strip()
            year, month = month_year.split('.')
            date = f"{year}/{month}/{day}"

            title = news.find('div', class_='wz').find('h2').text.strip()
            link = news.find('div', class_='wz').find('a').get('href')
            if link.startswith('..'):
                link = 'https://jwc.sjtu.edu.cn' + link[2:]

            summary = news.find('div', class_='wz').find('p').text.strip()

            result.append({
                'date': date,
                'title': title,
                'link': link,
                'summary': summary
            })
        except Exception as e:
            raise RuntimeError("Fail at function Academic.get_academic_news") from e
    return True, result
