import time, json
from utils.detect.detect_sensitives import DFAFilter, detect_sensitives
from utils.response import Response


def detect(request):
    """
    敏感词的过滤接口
    """
    # 计时器
    # time1 = time.time()
    # print('time1', time1)
    # 获取前端数据
    data = request.body.decode('utf-8')
    data = json.loads(data)
    plain_text = data.get('text')
    result_text = detect_sensitives(plain_text)
    # 返回
    data = {
        "filted_text": result_text
    }
    # time2 = time.time()
    # print('time2', time2)
    # print('总共耗时：' + str(time2 - time1) + 's')
    return Response.Response(data=data)
