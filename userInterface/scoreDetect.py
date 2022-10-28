from score_requests import selectScore
import time, datetime, random
from log import log
from e_Mail import rebackTimeMail, nextTimeMail
from sentScores import sentScores
frmt = "%Y-%m-%d %H:%M:%S"


def fenGe(msgtext):
    fenge = "\n"
    fenge += "*" * 30 + datetime.datetime.now().strftime(frmt) + "*" * 50 + "\n"
    fenge += msgtext + "\n"
    return fenge


def rebackTime_def():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timenow = datetime.datetime.now()
    time1 = datetime.datetime.strptime(today + " 00:00:00", frmt)
    time2 = datetime.datetime.strptime(today + " 09:00:00", frmt)
    time3 = datetime.datetime.strptime(today + " 12:00:00", frmt)
    time4 = datetime.datetime.strptime(today + " 21:00:00", frmt)
    time5 = datetime.datetime.strptime(today + " 00:00:00", frmt) + datetime.timedelta(days=1)
    if time1 <= timenow < time2:
        rebackTime = time2
    elif time2 <= timenow < time3:
        rebackTime = nextTime_def()
    elif time3 < timenow <= time4 or time4 < timenow < time5:
        rebackTime = time2 + datetime.timedelta(days=1)
    return rebackTime


def nextTime_def():
    start = datetime.datetime.now() + datetime.timedelta(minutes=10)
    start = start.strftime(frmt)
    end = datetime.datetime.now() + datetime.timedelta(minutes=15)
    end = end.strftime(frmt)
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + random.random() * (etime - stime)
    ptime = int(ptime)
    randomDate = time.strftime(frmt, time.localtime(ptime))
    randomDate = datetime.datetime.strptime(randomDate, frmt)
    return randomDate


def scoreDetect(zkzh, name):
    while True:
        response = selectScore(zkzh, name)
        if response == 504:
            rebackTime = rebackTime_def()
            ret = rebackTimeMail(zkzh, rebackTime)
            if ret:
                logmsg = fenGe("邮件发送成功")
                print(logmsg)
                log(zkzh, logmsg)
            else:
                logmsg = fenGe("邮件发送失败")
                print(logmsg)
                log(zkzh, logmsg)
            while True:
                time.sleep(1)
                if datetime.datetime.now() < rebackTime:
                   continue
                else:
                    break
        elif response in [301, 302, 303, 304, 307, 400, 401, 403, 404, 500, 503] or response == "无成绩记录":
            nextTime = nextTime_def()
            if response == "无成绩记录":
                msgtext = '暂无成绩记录，将在 %s 重试' % (nextTime.strftime(frmt))
                logmsg = fenGe(msgtext)
                print(logmsg)
                log(zkzh, logmsg)
            else:
                ret = nextTimeMail(zkzh,nextTime, response)
                if ret:
                    logmsg = fenGe("邮件发送成功")
                    print(logmsg)
                    log(zkzh, logmsg)
                else:
                    logmsg = fenGe("邮件发送失败")
                    print(logmsg)
                    log(zkzh, logmsg)
            while True:
                time.sleep(1)
                if datetime.datetime.now() < nextTime:
                    continue
                else:
                    break
        elif response == 200:
            sentScores()
            break
