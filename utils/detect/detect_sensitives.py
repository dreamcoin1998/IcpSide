"""
Author: dawnerstart
Function: 敏感词过滤
Time: 2021-07-04
"""
from auth_user.models import Sensitives


class DFAFilter(object):
    """
        DFA算法
        思路：获取敏感词表--把敏感词表做成字典--传入检测文本--对文本的过滤
    """
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定

    def get_sensitive_list(self):
        """
        获取敏感词列表，从txt得到
        """
        # sensitive_objects = Sensitives.objects.all().sensitive_words
        sensitive_list = []
        with open('D:\OneDrive\桌面\Python\敏感词检测\minganci.txt', encoding='utf-8') as f:
            for i in f:
                sensitive_list.append(i)
        # print(sensitive_list)
        return (sensitive_list)

    def get_sensitive_list_1(self):
        """
        获取敏感词列表，从mysql得到
        """
        sensitive_list = Sensitives.objects.values_list('sensitive_words', flat = True)
        # print(sensitive_list)
        return sensitive_list

    def add(self, keyword):
        """
        添加敏感词
        """
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    # 敏感词表做成字典
    def parse(self, sensitive_list: list):
        for keyword in sensitive_list:
            self.add(str(keyword).strip())
        # print(self.keyword_chains)

    def filter(self, message, repl="*"):
        """
        # 敏感词的过滤
        """
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)


def detect_sensitives(plain_text: str):
    """
    @param plain_text 原始文本
    @return result_text 过滤文本
    """
    # 计时器
    # time1 = time.time()
    # 构造一个过滤对象
    gfw = DFAFilter()
    # 输入敏感词数组，从txt得到
    # sensitive_list = gfw.get_sensitive_list()
    # 输入敏感词数组， 从mysql得到
    sensitive_list = gfw.get_sensitive_list_1()
    # 敏感词数组做成字典
    gfw.parse(sensitive_list)
    # 对文本的过滤
    result_text = gfw.filter(plain_text)
    # 结果
    # print(plain_text)
    # print(result_text)
    # time2 = time.time()
    # print('总共耗时：' + str(time2 - time1) + 's')
    # 返回
    return result_text
