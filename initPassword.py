import csv
import json

import requests

url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}


def json_list_to_csv(json_list, file_path):
    # 指定要筛选的字段
    fieldnames = ['id', 'seq', 'key']

    filtered_list = []  # 存储筛选后的字典列表

    # 对于每个字典，筛选出指定字段的键值对，构造新的字典
    for item in json_list:
        filtered_item = {key: item[key] for key in fieldnames}
        filtered_list.append(filtered_item)

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入表头
        writer.writeheader()

        # 逐行写入筛选后的字典列表的数据
        writer.writerows(filtered_list)


# 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
def browserList():
    json_data = {
        "page": 0,
        "pageSize": 10
    }
    res = requests.post(f"{url}/browser/list",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)
    # json_list_to_csv(res['data']['list'], 'output.csv')
    return res


browserList()
