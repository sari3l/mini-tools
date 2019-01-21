# coding: utf-8
from netSpider import NetSpider
from database import selectexplorenode
from optparse import OptionParser
import config

opts = OptionParser()
opts.add_option('-i', '--id', action='store', default="", type="string", dest="opt_oid", help=u"原点用户oid，可在用户页面$CONFIG中获取")
opts.add_option('-c', '--continue', action='store_true', default=False, dest="opt_continue", help=u"继续中断的任务，可受--deep参数影响")
opts.add_option('-d', '--deep', action='store', default=1, type="int", dest="opt_deep", help=u"爬巡深度，默认为1只爬取原点用户")
opts.add_option('-C', '--cookies', action='store', default="", type="string", dest="opt_cookies",  help=u"爬虫用户完整cookie")


def continuetask(maxDeep=config.maxDeep):
    deep = 1
    while deep <= maxDeep:
        print '[+]Check deep %d' % deep
        for user in selectexplorenode(deep):
            NetSpider(user['oid'], user['deep'], user).start()
        print '[~]Clear deep %d' % deep
        deep += 1


def checkcookie(optCookieStr):
    if len(optCookieStr) > 0:
        config.setcookies(optCookieStr)
        print "[*]若将常用此 cookie，可在 config 中修改 cookiesStr 变量."
    elif len(config.cookiesStr) <= 0:
        print '[!]Need Cookie, Please Reset.'
        exit(1)


def checkuseroid(optOidStr):
    if len(optOidStr) > 0:
        NetSpider(optOidStr).start()
        return True
    return False


def parseoptions(options):
    checkcookie(options.opt_cookies)
    if checkuseroid(options.opt_oid):
        options.opt_continue = True
    if options.opt_continue:
        continuetask(options.opt_deep)


if __name__ == '__main__':
    try:
        options, args = opts.parse_args()
        parseoptions(options)
    except KeyboardInterrupt:
        print '[!]~Exiting~'
        exit(2)
