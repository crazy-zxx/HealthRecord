import re

import requests
from bs4 import BeautifulSoup

import execjs

'''
============================================    研究生管理系统一键健康打卡    =======================================================
'''

# 登录页面
login_url = 'http://ipass.qust.edu.cn/tpass/login?service=http%3A%2F%2Fgms.qust.edu.cn%2Flogin%2FssoLogin'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'ipass.qust.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'close'
}
main_page_resp = requests.get(login_url, headers=headers)
print(main_page_resp.status_code)

# 下次请求需要带着上次响应返回的 cookie
cookies = [x for x in re.split(';|,| ', main_page_resp.headers.get('Set-Cookie').strip("'")) if x != '']
# cookie 实际上只需要 JSESSIONID 和 Language 就行了
jl_cookie = '; '.join(sorted([c for c in cookies if 'Language' in c or 'JSESSIONID' in c]))

# 用户名
un = '4021110075'
# 密码
pd = '1934109821@zXX'
ul = str(len(un))
pl = str(len(pd))
execution = 'e1s1'
_eventId = 'submit'
# 解析登录页面，找到用于登录时提交的参数lt
soup = BeautifulSoup(main_page_resp.text, "html.parser")
lt = soup.find_all('input', {'id': 'lt'})[0].get('value')
print(lt)

# 编码用于登录时提交的参数rsa
# 读取、编译js文件
ctx = execjs.compile(open('EncodeDecode.js', encoding="utf-8").read())
# 执行js函数，call（函数名，参数1，参数2，...）
rsa = ctx.call('strEnc', un + pd + lt, "1", "2", "3")
print(rsa)


# 获取post提交数据时候的Content-Length的函数
def get_content_length(data):
    length = len(data.keys()) * 2 - 1
    total = ''.join(list(data.keys()) + list(data.values()))
    length += len(total)
    return length


# 登录时提交的数据
data = {
    'rsa': rsa,
    'ul': ul,
    'pl': pl,
    'lt': lt,
    'execution': execution,
    '_eventId': _eventId
}

headers = {
    'Host': 'ipass.qust.edu.cn',
    'Content-Length': str(get_content_length(data)),
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://ipass.qust.edu.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://ipass.qust.edu.cn/tpass/login?service=http%3A%2F%2Fgms.qust.edu.cn%2Flogin%2FssoLogin',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': jl_cookie,
    'Connection': 'close'
}
print(headers)

# 发送登录请求
resp = requests.post(login_url, headers=headers, data=data, allow_redirects=False)
print(resp.status_code)
print(resp.headers)
print(resp.headers.get("Location"))

# 登录过程会重定向多次，分别请求解析
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'gms.qust.edu.cn',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://ipass.qust.edu.cn/',
    'Connection': 'close'
}
resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
print(resp.status_code)
print(resp.headers)
print(resp.headers.get("Location"))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'gms.qust.edu.cn',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'http://ipass.qust.edu.cn/',
    'Connection': 'close'
}
resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
print(resp.status_code)
print(resp.headers)
print(resp.headers.get("Location"))

cookies = [x for x in re.split(';|,| ', resp.headers.get('Set-Cookie').strip("'")) if x != '']
j_cookie = '; '.join([c for c in cookies if 'JSESSIONID' in c])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'gms.qust.edu.cn',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://ipass.qust.edu.cn/',
    'Cookie': j_cookie
}
print(headers)
resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
print(resp.status_code)
print(resp.headers)
print(resp.headers.get("Location"))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'gms.qust.edu.cn',
    'Cookie': '; '.join(sorted([c for c in cookies if 'JSESSIONID' in c])),
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'http://ipass.qust.edu.cn/'
}
resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
print(resp.status_code)
print(resp.headers.get("Location"))

resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
print(resp.status_code)

# 第一级收集表外壳框架
mycoll_url = 'https://gms.qust.edu.cn/efm/collection/enterListMyCollection?categoryId=mrjkdk'
j_cookie = str([c for c in cookies if 'JSESSIONID' in c][0])
jsessionid_val = j_cookie.split('=')[1]
data = {'token': jsessionid_val}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'gms.qust.edu.cn',
    'Cookie': j_cookie
              + '; https%3A%2F%2Fgms.qust.edu.cn%2F=%7B%22admHistory%22%3A%7B%224021110075%22%3A%5B%7B%22url%22%3A%22login%2FenterMain%2Fgrzxgl%2FenterGrzx%22%2C%22name%22%3A%22%E4%B8%AA%E4%BA%BA%E4%B8%AD%E5%BF%83%22%7D%5D%7D%7D',
    'Content-Length': str(get_content_length(data)),
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://gms.qust.edu.cn/login/enterMain/efm/collection/enterListMyCollection?categoryId=mrjkdk',
}
resp = requests.post(mycoll_url, headers=headers, data=data)
print(resp.status_code)

# 第一级收集表内容
todo_url = 'https://gms.qust.edu.cn/efm/collection/enterListTodoCollection?categoryId=mrjkdk'
resp = requests.post(todo_url, headers=headers, data=data)
print(resp.status_code)
# print(resp.text)
soup = BeautifulSoup(resp.text, "html.parser")
# 第一级收集表id
parent_data_id = soup.find('a', text='填写').get('data-id')
print(parent_data_id)

if parent_data_id:
    # 第二级收集表
    list_url = 'https://gms.qust.edu.cn/efm/collection/enterListRepeatedCollectionData/' + parent_data_id
    resp = requests.post(list_url, headers=headers, data=data)
    print(resp.status_code)
    soup = BeautifulSoup(resp.text, "html.parser")
    # 第二级收集表id
    child_data_id = soup.find('a', text='填写').get('data-id')
    print(child_data_id)

    if child_data_id:
        # 要填写的收集表
        coll_url = 'https://gms.qust.edu.cn/efm/collection/enterAddCollectionData/' + child_data_id
        resp = requests.post(list_url, headers=headers, data=data)
        print(resp.status_code)

        # 收集表提交地址
        submit_url = 'https://gms.qust.edu.cn/efm/collection/submitCollectionData'
        # 提交数据
        data = {
            "id": None,
            "collectId": parent_data_id,
            "data": {
                "szd": "370212",
                "tw": "37.2℃及以下",
                "stzk": "健康",
                "zgfxq": "否",
                "mj": "否",
                "ysbl": "否",
                "yxgl": "否",
                "jkmys": "绿色",
                "cn": "是",
                "szd_text": "山东 - 青岛市 - 崂山区",
                "tw_text": "37.2℃及以下",
                "stzk_text": "健康",
                "zgfxq_text": "否",
                "mj_text": "否",
                "ysbl_text": "否",
                "yxgl_text": "否",
                "jkmys_text": "绿色",
                "cn_text": "是"
            },
            "collectChildId": child_data_id
        }
        # 提交收集表
        resp = requests.post(submit_url, headers=headers, data=data)
        print(resp.status_code)
        if resp.status_code == '200':
            print("打卡成功！")
        else:
            print("打卡失败，出现了一点点小问题！")

# 退出登录
logout_url = 'https://gms.qust.edu.cn/login/signout'
resp = requests.get(logout_url, headers=headers, allow_redirects=False)
print(resp.status_code)
