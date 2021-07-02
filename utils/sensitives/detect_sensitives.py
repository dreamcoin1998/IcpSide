import json, jieba, MySQLdb
from django.http import JsonResponse


def detect(request):
    try:
        data = request.body.decode('utf-8')
        print(1)
        data = json.loads(data)
        print(2)
        # 提取前端数据
        text = data.get('text')
        # # jieba分词
        # result = jieba.cut(text, cut_all=True, HMM=False)
        # print(result)
        # 获取敏感词库的数据：list_sensitives
        list_sensitives = []
        db = MySQLdb.connect("134.175.218.240", "icpside1", "IcpSidetest", "icpside1", charset='utf8mb4')
        cursor = db.cursor()
        command = "select sensitive_words from auth_user_sensitives"
        cursor.execute(command)
        results = cursor.fetchall()
        for row in results:
            list_sensitives.append(row[0])
        # 对每一个分词进行检测:list_text
        list_text = jieba.lcut(text, cut_all=False, HMM=False)
        # 若分词敏感，用相等数量的星号（*）代替
        for i in list_sensitives:
            if i in text:
                text = text.replace(i, '*' * len(i))
        # 返回数据
        text1 = {
            'filted_text':text
        }
        return JsonResponse(data = text1)
    except Exception as e:
        print(e)
        text1 = {
            'filted_text': 'ERROR!'
        }
        return JsonResponse(data = text1)

