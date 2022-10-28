import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
from tableProcess import tableProcess
from models import Students
from log import log
import gzip
from io import BytesIO
from e_Mail import Mail
import datetime


host = 'smtp.exmail.qq.com'
passwd = 'Long19990224'
from_addr = '2017083122@czie.edu.cn'
frmt = "%Y-%m-%d %H:%M:%S"


def fenGe(msgtext):
    fenge = "\n"
    fenge += "*" * 30 + datetime.datetime.now().strftime(frmt) + "*" * 50 + "\n"
    fenge += msgtext + "\n"
    return fenge

# https://www.jseea.cn/webfile/examination/selflearning/
# https://sdata.jseea.cn/tpl_front/score/practiceScoreList.html
# https://sdata.jseea.cn/tpl_front/score/allScoreList.html
def toZiKao(zkzh):
    url = "https://www.jseea.cn/webfile/examination/selflearning/"
    headers = {
        'Host': 'www.jseea.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': 1,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
    }

    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url=url, headers=headers)
    try:
        logmsg = fenGe("尝试访问：" + url)
        log(zkzh, logmsg)
        response = opener.open(request)
        cookie_str = ""
        for item in cookie:
            cookie_str += item.name + "=" + item.value + ";"
        cookie = cookie_str.rstrip(";")
        logmsg = fenGe(url + "的Cookie：\n" + cookie)
        log(zkzh, logmsg)
        q = Students.objects.filter(zkzh=zkzh)
        q.setCookie(cookie)
        return cookie
    except urllib.error.HTTPError as e:
        msg = 'code: ' + str(e.code) + '\n'
        msg += 'reason: ' + e.reason + '\n'
        msg += 'headers: {\n' + str(e.headers) + '}\n'
        logmsg = fenGe(msg)
        log(zkzh, logmsg)
        ret = Mail(zkzh, e.code, msg, '')
        if ret:
            logmsg = fenGe("邮件发送成功")
            log(zkzh, logmsg)
        else:
            logmsg = fenGe("邮件发送失败")
            log(zkzh, logmsg)
        return e.code


def toSelectScore(zkzh, cookie):
    url = "https://sdata.jseea.cn/tpl_front/score/practiceScoreList.html"
    headers = {
        'Host': 'sdata.jseea.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.jseea.cn/selflearning.html',
        'DNT': 1,
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': 1,
        'Cache-Control': 'max-age=0'
    }

    cookie1 = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie1)
    opener = urllib.request.build_opener(handler)
    request = urllib.request.Request(url=url, headers=headers)
    try:
        logmsg = fenGe("尝试访问：" + url)
        log(zkzh, logmsg)
        response = opener.open(request)
        cookie_str = cookie + ";"
        for item in cookie1:
            cookie_str += item.name + "=" + item.value + ";"
        cookie = cookie_str.rstrip(";")
        logmsg = fenGe(url + "的Cookie：\n" + cookie)
        log(zkzh, logmsg)
        q = Students.objects.filter(zkzh=zkzh)
        q.setCookie(cookie)
        return cookie
    except urllib.error.HTTPError as e:
        msg = 'code: ' + str(e.code) + '\n'
        msg += 'reason: ' + e.reason + '\n'
        msg += 'headers: {\n' + str(e.headers) + '}\n'
        logmsg = fenGe(msg)
        log(zkzh, logmsg)
        if e.code == 504:
            return 504
        else:
            ret = Mail(zkzh, e.code, msg, '')
            if ret:
                logmsg = fenGe("邮件发送成功")
                log(zkzh, logmsg)
            else:
                logmsg = fenGe("邮件发送失败")
                log(zkzh, logmsg)


def selectScore(zkzh, name):
    cookie = Students.objects.filter(zkzh=zkzh).values("cookies")[0]["cookies"]
    if cookie:
        if cookie.cookieIs_timeout:
            cookie = toZiKao(zkzh)
            cookie = toSelectScore(zkzh, cookie)
    else:
        cookie = toZiKao(zkzh)
        cookie = toSelectScore(zkzh, cookie)
    if cookie in [301, 302, 303, 304, 307, 400, 401, 403, 404, 500, 503, 504]:
        return cookie
    url = 'https://sdata.jseea.cn/tpl_front/score/allScoreList.html'
    params = {
        'zkzh': zkzh,
        'ksmx': name
    }
    headers = {
        'Host': 'sdata.jseea.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': 41,
        'Origin': 'https://sdata.jseea.cn',
        'DNT': 1,
        'Connection': 'keep-alive',
        'Referer': 'https://sdata.jseea.cn/tpl_front/score/practiceScoreList.html',
        'Cookie': cookie,
        'Upgrade-Insecure-Requests': 1,
    }
    data = bytes(urllib.parse.urlencode(params), encoding='utf8')
    try:
        logmsg = fenGe("尝试访问：" + url)
        log(zkzh, logmsg)
        request = urllib.request.Request(url, data)
        for i in headers:
            request.add_header(i, headers[i])
        response = urllib.request.urlopen(request)
        htmls = response.read()
        buff = BytesIO(htmls)
        f = gzip.GzipFile(fileobj=buff)
        htmls = f.read().decode('utf-8')
        htmls = tableProcess(htmls)
        logmsg = fenGe(htmls)
        log(zkzh, logmsg)
        if "2021年07月03日" not in htmls:
            return "无成绩记录"
        else:
            Mail(zkzh, 200, "似乎有成绩了", htmls)
            return 200

    except urllib.error.HTTPError as e:
        msg = 'code: ' + str(e.code) + '\n'
        msg += 'reason: ' + e.reason + '\n'
        msg += 'headers: {\n' + str(e.headers) + '}\n'
        logmsg = fenGe(msg)
        log(zkzh, logmsg)
        ret = Mail(zkzh, e.code, msg, '')
        if ret:
            logmsg = fenGe("邮件发送成功")
            log(zkzh, logmsg)
        else:
            logmsg = fenGe("邮件发送失败")
            log(zkzh, logmsg)
        return e.code

