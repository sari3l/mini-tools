# coding: utf-8
import config
import re
import requests
from bs4 import BeautifulSoup
from database import createrelation, updatenode
from sClass import User, Topic


class NetSpider(object):

    def __init__(self, uid=0, parentdeep=0, node={}):
        self.user = User()
        self.user.oid = uid
        self.user.deep = parentdeep + 1
        self.user.__dict__ = dict(self.user.__dict__, **node)
        self.docHTML = None
        self.userDict = self.user.__dict__
        self.infoUrl = ['https://weibo.com', 'http:']

    def start(self):
        print "[*]Crawling user %s" % self.user.oid
        self.beforestart()
        self.getinfo()
        self.afterstart()

    def beforestart(self):
        self.getdochtml('baseLink', self.user.oid)
        doc = self.docHTML.head.getText()
        if self.user.oid != config.defaultValue:
            self.user.oid = re.findall(r"CONFIG\['oid'\]='(\d+)'", doc)[0]
        self.user.url = "https://weibo.com/" + self.user.oid
        self.user.pageid = re.findall(r"CONFIG\['page_id'\]='(\d+)'", doc)[0]
        self.user.domain = re.findall(r"CONFIG\['domain'\]='(\d+)'", doc)[0]
        if self.user.avatar == config.defaultValue:
            self.user.avatar = "https:" + self.docHTML.find('img', class_='photo')['src']
        url = self.docHTML.find('a', class_="WB_cardmore")['href']
        self.infoUrl = self.infoUrl['weibo.com' in url] + url

    def afterstart(self):
        self.user.isExploded = True
        updatenode(self.user)

    def getdochtml(self, stype=None, sid="", extra="", fullurl=None):
        if fullurl is not None:
            url = fullurl
        else:
            url = config.links[stype].replace('<payload>', sid) + extra
        rep = requests.get(url, headers=config.headers, cookies=config.cookies, allow_redirects=True)
        self.docHTML = BeautifulSoup(rep.text, 'lxml')

    def getinfo(self):
        self.getcommoninfo()
        if 'about' in self.infoUrl:
            self.getoffcialinfo()
        else:
            self.getuserinfo()
        if self.user.domain == u'100505':
            self.getsocialnetwork()
        elif self.user.domain not in config.ignoreDomain:
            print '[!]用户 `%s` 存在 domain `%s`, 需要手工检查' % (self.user.name.encode('utf-8'), self.user.domain.encode('utf-8'))

    def getuserinfo(self):
        try:
            infoHTML = self.docHTML.find('div', class_='WB_frame_c').find_all('div', class_="WB_cardwrap")
            for singleInfo in infoHTML:
                singleInfoKey = singleInfo.find('div', class_="obj_name").string
                singleInfoValue = singleInfo.find('div', class_='WB_innerwrap')
                self.parseinfodata(singleInfoKey, singleInfoValue)
        except Exception as e:
            print '[!]非标准用户，停止爬取 `%s` 个人信息, 报错内容 -> %s' % (str(self.user.oid), e.message)

    def getoffcialinfo(self):
        try:
            infoHTML = self.docHTML.find('div', class_='WB_frame_c').find('div', class_="WB_cardwrap")
            key = infoHTML.find('h2', class_="main_title").string
            value = infoHTML.find('p', class_="p_txt").string
            self.parseinfodata(key, value)
        except:
            print '[!]账号 `%s` 无简介等信息' % self.user.name.encode('utf-8')

    def getcommoninfo(self):
        self.getdochtml(fullurl=self.infoUrl)
        try:
            self.user.level = self.docHTML.find('a', class_='W_icon_level').span.string
        except:
            print '[!]可能为 `%s` 官方账号，无等级信息' % self.user.name.encode('utf-8')

    def getsocialnetwork(self):
        self.getdochtml('followsLink', self.user.pageid)
        for num in self.docHTML.find_all('a', attrs={'action-type': 'nav_lev'}):
            self.parseinfodata(num.span.string, num.find('em', 'num').string)
        self.getallusers('follows')
        self.getallusers('fans')

    def parseinfodata(self, key, html):
        if key == u'基本信息':
            for sibling in html.ul.find_all('li'):
                stringList = [i for i in sibling.stripped_strings]
                self.userDict[config.baseInfoDict[stringList[0]]] = stringList[1]
        elif key == u'工作信息':
            self.user.company = [i for i in html.stripped_strings]
        elif key == u'教育信息':
            self.user.education = [i for i in html.stripped_strings]
        elif key == u'标签信息':
            self.user.tags = [i for i in html.stripped_strings]
        elif u'关注' in key:
            self.user.followsNum = int(html)
        elif u'粉丝' in key:
            self.user.fansNum = int(html)
        elif key == u'简介':
            self.user.introduction = html

    def getPageNum(self, type):
        num = self.userDict[type + 'Num']
        page = num / 20 + (1 if num % 20 > 0 else 0)
        if config.maxPagelimit is True and page > config.maxPage:
            page = config.maxPage
        return page

    def getallusers(self, type):
        for i in xrange(self.getPageNum(type)):
            print '[*]Crawling page %s %s %d' % (self.user.oid, type, i+1)
            self.getdochtml(type+'Link', self.user.pageid, config.page[type] + str(i + 1))
            self.getfollowsinfo(type)

    def getfollowsinfo(self, type):
        followList = self.docHTML.find('ul', 'follow_list')
        for singleUser in followList.find_all('dt', class_='mod_pic'):
            singleUserInfo = singleUser.find('img')
            # 这个if有问题
            if "/p/" in singleUser.a['href']:
                print '[!]检测到超级话题 `%s`' % singleUser.a['title'].encode('utf-8')
                user = Topic()
                user.oid = re.findall('\/p\/(\w+)', singleUser.a['href'])[0]
                type = 'focuson'
            else:
                user = User()
                user.deep = self.user.deep + 1
                user.oid = re.findall('id=(\d+)&', singleUserInfo['usercard'])[0]
            user.avatar = "https:" + singleUserInfo['src']
            user.name = singleUser.a['title']
            createrelation(self.user, user, type)
