import requests
import json

url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}


def open_browser(id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
    json_data = {"id": f'{id}'}
    res = requests.post(f"{url}/browser/open",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)
    print(res['data']['http'])
    return res

def browser_list():
    json_data = {
        "page": 0,
        "pageSize": 10
    }
    res = requests.post(f"{url}/browser/list",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)
    return res

def send_post_request(id):
    print('请求开始')

    data = {
        "id": id,
        "args": [],
        "loadExtensions": True
    }

    response = requests.post(f"{url}/browser/open", json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        print('请求成功')
        print('返回的内容：', response.json())
        driver_path = response_data['data']['driver']  # 提取'driver'字段的值
        print('驱动路径：', driver_path)
    else:
        print('请求失败，状态码：', response.status_code)

    return response.json()
