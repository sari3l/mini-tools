# coding: utf-8

# 用户cookies
cookiesStr = ''''''                 # 默认cookie填充字段
cookies = None                      # 自动填充，勿修改

# 数据库
datauser = "neo4j"
datapass = "123456"

# 默认未填充数据值
defaultValue = u"未填写"

# 基本信息字段，建议在User类中添加相应变量，否则只有存在时才会向数据库中写入
baseInfoDict = {
    u'血型：': 'blood',
    u'生日：': 'birth',
    u'真实姓名：': 'realname',
    u'博客：': 'blog',
    u'昵称：': 'name',
    u'所在地：': 'location',
    u'性别：': 'sex',
    u'个性域名：': 'website',
    u'简介：': 'intro',
    u'注册时间：': 'registeredTime',
    u'感情状况：': 'singledog',
    u'性取向：': 'sexual',
}

# 爬虫设置
max_deep = 3                        # 默认爬虫深度
headers = {                         # 爬虫header
    "user-agent": "spider"
}
maxPagelimit = True                 # 是否有最大查看页数限制
maxPage = 5                         # 限制最大页数

page = {
    'fans': '&page=',               # 粉丝页面翻页参数
    'follows': '?page='             # 关注页面翻页参数
}
ignoreDomain = [u'100606']          # 忽略的$CONFIG.domain值

# 主要爬取链接
links = {
    'baseLink': "https://weibo.com/<payload>",
    'aboutLink': "https://weibo.com/<payload>/about",
    'infoLink': "https://weibo.com/p/<payload>/info",
    'fansLink': "https://weibo.com/p/<payload>/follow?relate=fans",
    'followsLink': "https://weibo.com/p/<payload>/follow"
}

# cookie 转换
def setcookies(cookiestr):
    global cookies
    cookies = dict([one.split('=', 1) for one in cookiestr.replace(' ', '').split(';')])
