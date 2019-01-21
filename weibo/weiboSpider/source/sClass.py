# coding: utf-8
from config import defaultValue, baseInfoDict


class User(object):

    def __init__(self):
        # 基础属性
        self.domain = defaultValue
        self.oid = defaultValue
        self.url = defaultValue
        self.pageid = defaultValue  # domain + oid 对于一些用户非此生成
        self.followsNum = 0
        self.fansNum = 0
        self.level = defaultValue
        self.avatar = defaultValue

        # 个人信息
        for v in baseInfoDict.values():
            self.__dict__[v] = defaultValue

        # 企业用户
        self.introduction = defaultValue

        # 工作信息
        self.company = defaultValue

        # 教育信息
        self.education = defaultValue

        # 标签信息
        self.tags = defaultValue

        # 爬虫属性
        self.deep = 0
        self.isExploded = False


class Topic(object):

    def __init__(self):
        self.oid = defaultValue
        self.name = defaultValue
        self.avatar = defaultValue
        self.isExploded = True
