import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import execjs

'''
============================================    研究生管理系统一键健康打卡    =======================================================
'''
# ------------------  只需要在此处设置你的智慧青科大账号和密码即可   ------------------------
# 用户名
un = '4021110075'
# 密码
pd = '1934109821@zXX'

# 登录页面
login_url = 'http://ipass.qust.edu.cn/tpass/login?service=http%3A%2F%2Fgms.qust.edu.cn%2Flogin%2FssoLogin'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'ipass.qust.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'close'
}
main_page_resp = requests.get(login_url, headers=headers)
if main_page_resp.status_code == 200:
    print('解析登录页面成功！')

# 下次请求需要带着上次响应返回的 cookie
cookies = [x for x in re.split(';|,| ', main_page_resp.headers.get('Set-Cookie').strip("'")) if x != '']
# cookie 实际上只需要 JSESSIONID 和 Language 就行了
jl_cookie = '; '.join(sorted([c for c in cookies if 'Language' in c or 'JSESSIONID' in c]))

ul = str(len(un))
pl = str(len(pd))
execution = 'e1s1'
_eventId = 'submit'
# 解析登录页面，找到用于登录时提交的参数lt
soup = BeautifulSoup(main_page_resp.text, "html.parser")
lt = soup.find_all('input', {'id': 'lt'})[0].get('value')

# 编码用于登录时提交的参数rsa。其实就是对登录的用户账号信息进行了加密
# 读取、编译js文件
ctx = execjs.compile(open('EncodeDecode.js', encoding="utf-8").read())
# 执行js函数，call（函数名，参数1，参数2，...）
rsa = ctx.call('strEnc', un + pd + lt, "1", "2", "3")


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

# 发送登录请求
resp = requests.post(login_url, headers=headers, data=data, allow_redirects=False)
if resp.status_code == 302:
    print('开始登录！')
    print('重定向到：', resp.headers.get("Location"))

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
if resp.status_code == 302:
    print('重定向到：', resp.headers.get("Location"))

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
if resp.status_code == 302:
    print('重定向到：', resp.headers.get("Location"))

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
resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
if resp.status_code == 302:
    print('重定向到：', resp.headers.get("Location"))

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
if resp.status_code == 302:
    print('重定向到：', resp.headers.get("Location"))

resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
if resp.status_code == 200:
    print('登录成功！')

print('正在打卡...学校网站慢，请耐心等待，可能需要1分钟左右！')

# 第一级收集表外壳框架
mycoll_url = 'https://gms.qust.edu.cn/efm/collection/enterListMyCollection?categoryId=mrjkdk'
j_cookie = str([c for c in cookies if 'JSESSIONID' in c][0])
jsessionid_val = j_cookie.split('=')[1]
data = {'token': jsessionid_val}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'gms.qust.edu.cn',
    'Cookie': j_cookie,
    'Content-Length': str(get_content_length(data)),
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://gms.qust.edu.cn/login/enterMain/efm/collection/enterListMyCollection?categoryId=mrjkdk'
}
resp = requests.post(mycoll_url, headers=headers, data=data)

# 第一级收集表内容
todo_url = 'https://gms.qust.edu.cn/efm/collection/enterListTodoCollection?categoryId=mrjkdk'
resp = requests.post(todo_url, headers=headers, data=data)
soup = BeautifulSoup(resp.text, "html.parser")
# 第一级收集表id
parent_data_id = soup.find('a', text='填写').get('data-id')

if parent_data_id:
    # 第二级收集表
    list_url = 'https://gms.qust.edu.cn/efm/collection/enterListRepeatedCollectionData/' + quote(parent_data_id, 'utf-8')
    resp = requests.post(list_url, headers=headers, data=data)
    soup = BeautifulSoup(resp.text, "html.parser")
    # 第二级收集表id
    child_data_id = soup.find('a', text='填写').get('data-id')

    if child_data_id:
        # 要填写的收集表
        coll_url = 'https://gms.qust.edu.cn/efm/collection/enterAddCollectionData/' + quote(child_data_id, 'utf-8')
        resp = requests.post(list_url, headers=headers, data=data)

        # 收集表提交地址
        submit_url = 'https://gms.qust.edu.cn/efm/collection/submitCollectionData'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'Host': 'gms.qust.edu.cn',
            'Cookie': j_cookie,
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://gms.qust.edu.cn/login/enterMain/efm/collection/enterListMyCollection?categoryId=mrjkdk',
            'Content - Type': 'application / json'
        }
        # ---------------------  提交数据，固定格式请勿乱动！！！ ---------------------
        data = {
            "id": None,
            "collectId": parent_data_id,
            "data": {
                "szd": "370212",  # 所在地。。崂山区370212，至于其他城市有时间再添加
                "tw": "37.2℃及以下",  # 体温。。仅可自行修改为：37.2℃及以下、37.3℃-37.9℃、38℃及以上
                "stzk": "健康",  # 身体状况。。仅可自行修改为：健康、发烧、干咳、乏力、其他
                "zgfxq": "否",  # 近14天你或你的共同居住人是否有疫情中、高风险区域人员接触史。。仅可自行修改为：是、否
                "mj": "否",  # 近14天你或你的共同居住人是否和确诊、疑似病人接触过。。仅可自行修改为：是、否
                "ysbl": "否",  # 近14天你或你的共同居住人是否是确诊、疑似病例。。仅可自行修改为：是、否
                "yxgl": "否",  # 你和你的共同居住人目前是否被医学隔离。。仅可自行修改为：是、否
                "jkmys": "绿色",  # 今天你当地的健康码颜色是。。仅可自行修改为：绿色、黄色、红色
                "cn": "是",  # 本人是否承诺以上所填报内容属实、准确，不存在任何隐瞒与不实情况，更无遗漏之处。。仅可自行修改为：是、否
                "szd_text": "山东 - 青岛市 - 崂山区",  # 所在地全称：山东 - 青岛市 - 崂山区，以下数据信息同上
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
        # 提交收集表, 此处需要提交 json 类型数据
        resp = requests.post(submit_url, headers=headers, json=data)
        if resp.status_code == 200:
            print("打卡成功！")
        else:
            print("打卡失败，出现了一点点小问题！等会再试一次？如果一直有问题就自己去手动打卡吧！")
    else:
        print('没有解析到需要填写的打卡！')
else:
    print('没有解析到需要填写的打卡信息收集！')

# 退出登录
logout_url = 'https://gms.qust.edu.cn/login/signout'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'Host': 'gms.qust.edu.cn',
    'Cookie': j_cookie,
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://gms.qust.edu.cn/login/enterMain/'
}
resp = requests.get(logout_url, headers=headers, allow_redirects=False)
resp = requests.get(resp.headers.get("Location"), headers=headers, allow_redirects=False)
if resp.status_code == 302:
    print('退出登录完成！')
