# jHelper

## Academic Functions

### `get_selected_course_list` Function

`get_selected_course_list(year,semester,driver)` has **3** parameters:

- `year` is an **integer** that represents year of semester.
- `semester` is an **integer** that represents semester, and only **1**, **2** and **3** are valid. 1 for **fall** semester, 2 for **spring** semester and 3 for **summer** semester.
- `driver` is the webdriver that your jAccount logged in.

The function returns a list of courses which displays in dictionary like:

```python
{
    'bh_id': '114514SJTU1919810ACADEMIC1919810',
    'bjdm': '电院2472',
    'bjmc': '电院2472',
    'cdlbmc': '不排教室',
    'cxbj': '否',
    'czr': '19198/野先辈',
    'date': '二○二五年五月十四日',
    'dateDigit': '2025年5月14日',
    'dateDigitSeparator': '2025-5-14',
    'day': '14',
    'fxbj': '无',
    'jcytbj': '否',
    'jfzt': '未缴',
    'jg_id': '03001',
    'jgdm': '03001',
    'jgmc': '计算机学院',
    'jgpxzd': '1',
    'jsgh': '19198',
    'jsmc': '野先辈',
    'jsxx': '19198/野先辈/副教授(高校思政)',
    'jxb_id': '114514SJTU1919810ACADEMIC1919810',
    'jxbmc': '(2024-2025-2)-PSY1145-14',
    'jxbzc': '2024计算机科学与技术',
    'jxdd': '不排教室',
    'kcfl': '公共课',
    'kch': 'PSY1145',
    'kch_id': 'PSY1145',
    'kclbdm': '41',
    'kclbmc': '公共课程类',
    'kcmc': '大学生心理健康',
    'kcsfzk': '收费',
    'kcxzmc': '必修',
    'kcywmc': "University Student's  Mental Health",
    'kklxdm': '01',
    'kklxmc': '主修课程',
    'kkxy_id': '11451',
    'kkxydm': '11451',
    'kkxymc': '学指委（学生处、团委、人武部）合署',
    'kkzt': '1',
    'kkztmc': '开课',
    'listnav': 'false',
    'localeKey': 'zh_CN',
    'month': '5',
    'njdm_id': '2024',
    'njmc': '2024',
    'pageTotal': 0,
    'pageable': True,
    'qsjsz': '1-16周',
    'queryModel': 
        {
            'currentPage': 1,
            'currentResult': 0,
            'entityOrField': False,
            'limit': 15,
            'offset': 0,
            'pageNo': 0,
            'pageSize': 15,
            'showCount': 10,
            'sorts': [],
            'totalCount': 0,
            'totalPage': 0,
            'totalResult': 0
        },
    'rangeable': True,
    'row_id': '1',
    'rwzxs': '32',
    'sfjf': '未缴',
    'sfzx': '在校',
    'sjhm': '11451419198',
    'skfs': '中文',
    'sksj': '星期三第6-6节{1-16周}',
    'totalResult': '16',
    'userModel': 
        {
            'monitor': False,
            'roleCount': 0,
            'roleKeys': '',
            'roleValues': '',
            'status': 0,
            'usable': False
        },
    'xbm': '1',
    'xbmc': '男',
    'xdcs': '2',
    'xf': '1',
    'xh': '524031919810',
    'xh_id': '524031919810',
    'xjydmc': '无',
    'xjztmc': '正常在校',
    'xkbjmc': '管配',
    'xkcx_id': '114514SJTU1919810ACADEMIC1919810-524031919810',
    'xklcmc': '试选',
    'xksj': '2024-12-18 11:04:23',
    'xm': '兽先辈',
    'xnm': '2024',
    'xnmc': '2024-2025',
    'xqh': '02',
    'xqh_id': '02',
    'xqhmc': '闵行',
    'xqm': '12',
    'xqmc': '2',
    'xslbmc': '本科生(中国国籍)',
    'xsmc': '其他',
    'xxlx': '0',
    'xxlxmc': '正常',
    'xxzykbj': '否',
    'xzmc': '4',
    'year': '2025',
    'zjhm': '11451419190810001X',
    'zxbj': '否',
    'zy': '1',
    'zydm': '080601',
    'zyfxmc': '无方向',
    'zyh_id': '080601',
    'zymc': '计算机科学与技术'
}

```