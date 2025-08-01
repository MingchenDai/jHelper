import requests
import Files
import re
import json


# 0 for Main Library
# 1 for TDL Library
# 2 for YKP Library
# 3 for Xuhui Reading Room
def get_library_statics():
    try:
        response = requests.get('https://zgrstj.lib.sjtu.edu.cn/cp')
        json_str = re.search(r'CountPerson\((.*)\);', response.text, re.DOTALL).group(1)
        data_list = json.loads(json_str)['numbers']
        return_list=[]
        for item in data_list:
            return_list.append([item['areaName'],int(item['inCounter']),int(item['max'])])
        return return_list
    except Exception as e:
        raise RuntimeError(Files.exception_throw_out()) from e


def get_library_number_current() -> tuple[int, int, int, int] | None:
    try:
        response = requests.get('https://zgrstj.lib.sjtu.edu.cn/cp')
        json_str = re.search(r'CountPerson\((.*)\);', response.text, re.DOTALL).group(1)
        number_list = json.loads(json_str)['numbers']
        return int(number_list[0]['inCounter']), int(number_list[1]['inCounter']), int(
            number_list[2]['inCounter']), int(number_list[3]['inCounter'])
    except Exception as e:
        RuntimeError(Files.exception_throw_out(), e)


def get_library_number_max():
    try:
        response = requests.get('https://zgrstj.lib.sjtu.edu.cn/cp')
        json_str = re.search(r'CountPerson\((.*)\);', response.text, re.DOTALL).group(1)
        number_list = json.loads(json_str)['numbers']
        return int(number_list[0]['max']), int(number_list[1]['max']), int(number_list[2]['max']), int(
            number_list[3]['max'])
    except Exception as e:
        RuntimeError(Files.exception_throw_out(), e)


print(get_library_statics())
