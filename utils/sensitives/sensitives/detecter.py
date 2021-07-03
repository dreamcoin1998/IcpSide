"""
检测敏感词——后端使用
"""
import json, jieba, MySQLdb, pymysql
from django.http import JsonResponse

def detect(data:str):
    print(type(data), '1~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(data)
    # 获取敏感词库的数据：list_sensitives
    list_sensitives = []
    db = pymysql.connect("134.175.218.240", "icpside1", "IcpSidetest", "icpside1")
    cursor = db.cursor()
    command = "select sensitive_words from auth_user_sensitives"
    cursor.execute(command)
    results = cursor.fetchone()
    # 对每一个分词进行检测
    for row in results:
        list_sensitives.append(row[0])
    print('敏感词表', list_sensitives)
    # 若分词敏感，用相等数量的星号（*）代替
    for i in list_sensitives:
        if i in data:
            data = data.replace(i, '*' * len(i))
    # 返回数据
    return (data)

data = '习近平'
print(detect(data))
