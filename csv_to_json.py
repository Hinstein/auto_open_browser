import csv
import json


def csv_to_json(csv_file):
    # 打开CSV文件并读取数据
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    result = {}

    for item in data:
        seq = item['seq']
        id = item['id']
        password = item['password']
        result[seq] = {'id': id, 'password': password}
        # 返回数据
    print(result)
    return result


# # 指定CSV文件路径
# csv_file = 'output.csv'
#
# csv_to_json(csv_file)
