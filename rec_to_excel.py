# -*- coding: utf-8 -*-
# @Time     : 2020/7/17
# @Author   : Long
import re
import pandas as pd
from pymongo import MongoClient


def rec_to_mongo():
    db_local = MongoClient('localhost', 27017)['llf']
    client = db_local['xinguan_0720']
    f2 = open("xinguan.txt", "r", encoding='utf-8')
    lines = f2.readlines()
    ls = []
    dic = {}
    # dic最后插入的字典键值
    dic_key = ""
    num = len(lines)
    print(num)
    for line in lines:
        if '<REC>' in line:
            if dic:
                ls.append(dic)
                if len(ls) % 500 == 0:
                    client.insert_many(ls)
                    ls = []
            dic = {}
        elif re.findall("<(.*?)>=([\s\S]*)", line):
            k, v = re.findall("<(.*?)>=([\s\S]*)", line)[0]
            dic[k] = v
            # 把最近的一次key记录下来
            dic_key = k
        # 如果不是<REC>且没有匹配到<>=标签，把该行追加到最新的key-value中
        else:
            dic[dic_key] += line
        # 最后一行没有<REC>需要单独添加
        num -= 1
        if num == 0:
            ls.append(dic)
    client.insert_many(ls)


def rec_to_excel():
    f2 = open("xinguan.txt", "r", encoding='utf-8')
    lines = f2.readlines()
    ls = []
    dic = {}
    # dic最后插入的字典键值
    dic_key = ""
    num = len(lines)
    print(num)
    for line in lines:
        if '<REC>' in line:
            if dic:
                ls.append(dic)
            dic = {}
        elif re.findall("<(.*?)>=([\s\S]*)", line):
            k, v = re.findall("<(.*?)>=([\s\S]*)", line)[0]
            dic[k] = v
            # 把最近的一次key记录下来
            dic_key = k
        # 如果不是<REC>且没有匹配到<>=标签，把该行追加到最新的key-value中
        else:
            dic[dic_key] += line
        # 最后一行没有<REC>需要单独添加
        num -= 1
        if num == 0:
            ls.append(dic)
    pf = pd.DataFrame(ls)
    pf.to_excel("xinguan1.xlsx", engine='xlsxwriter')


if __name__ == '__main__':
    rec_to_excel()

