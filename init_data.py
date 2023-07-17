import requests
from tinydb import TinyDB, Query

import initPassword

url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}

def init_data(db):
    # 插入数据
    ori_data = initPassword.browserList()
    datajson = ori_data['data']['list']
    print(datajson)

    # 指定要筛选的字段
    fieldnames = ['id', 'seq']

    # 查询数据
    User = Query()

    # 对于每个字典，筛选出指定字段的键值对，构造新的字典
    for item in datajson:
        filtered_item = {key: item[key] for key in fieldnames}

        # 添加新的键，并将其值设置为空
        filtered_item['metamask'] = None

        # 查询是否已存在相同的seq
        existing_doc = db.get(User.seq == item['seq'])

        if existing_doc is None:
            # 不存在相同的seq，则插入文档
            db.insert(filtered_item)
        else:
            # 存在相同的seq，则不更新文档
            print(f"Document with seq {item['seq']} already exists, skipping update.")

    all_data = db.all()
    # 打印查询结果
    for document in all_data:
        print(document)


# 创建数据库实例
db = TinyDB('data.json')

# 调用 init_data() 函数，并传递数据库实例作为参数
init_data(db)

# 关闭数据库连接
db.close()
