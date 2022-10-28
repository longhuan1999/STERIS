import datetime
import smtplib
from models import Students
from email.mime.text import MIMEText
from email.utils import formataddr
from log import log
frmt = "%Y-%m-%d %H:%M:%S"
host = 'smtp.exmail.qq.com'
passwd = 'Long19990224'
from_addr = '2017083122@czie.edu.cn'
from_addr_name = 'endless小龙的自考成绩查询系统'
admin_addr = '2114467924@qq.com'


def fenGe(msgtext):
    fenge = "\n"
    fenge += "*" * 30 + datetime.datetime.now().strftime(frmt) + "*" * 50 + "\n"
    fenge += msgtext + "\n"
    return fenge


def signupMail(zkzh, signup_info):
    ret = True
    try:
        if zkzh != "024920431210":
            to_addr = Students.objects.filter(zkzh=zkzh).values("student_email")[0]["student_email"]
            to_addr_name = Students.objects.filter(zkzh=zkzh).values("student_name")[0]["student_name"]
            logmsg = fenGe("给%s的邮箱%s发送注册成功信息" % (to_addr_name, to_addr))
            log("024920431210", logmsg)
        elif zkzh == "024920431210":
            to_addr = admin_addr
            to_addr_name = "管理员"
            logmsg = fenGe("给%s的邮箱%s发送注册成功信息" % (to_addr_name, to_addr))
            log("024920431210", logmsg)
        msgtext = signup_info
        msg = MIMEText(msgtext, 'html', 'utf-8')
        msg['From'] = formataddr([from_addr_name, from_addr])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([to_addr_name, to_addr])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "注册成功"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(host, 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(from_addr, passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(from_addr, [to_addr, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def ipLocationMail(msg):
    ret = True
    try:
        msgtext = 'IP地址归属查询接口异常:\n%s' % (msg)
        msg = MIMEText(msgtext, 'plain', 'utf-8')
        msg['From'] = formataddr([from_addr_name, from_addr])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["管理员", admin_addr])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "IP地址归属查询接口异常"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(host, 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(from_addr, passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(from_addr, [admin_addr, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def rebackTimeMail(zkzh, rebackTime):
    ret = True
    try:
        msgtext = '检测到504，官方自考成绩查询入口已关闭，将在 %s 重试' % (rebackTime.strftime(frmt))
        logmsg = fenGe(msgtext)
        
        log(zkzh, logmsg)
        if zkzh != "024920431210":
            to_addr = Students.objects.filter(zkzh=zkzh).values("student_email")[0]["student_email"]
            to_addr_name = Students.objects.filter(zkzh=zkzh).values("student_name")[0]["student_name"]
        elif zkzh == "024920431210":
            to_addr = admin_addr
            to_addr_name = "管理员"
        msg = MIMEText(msgtext, 'plain', 'utf-8')
        msg['From'] = formataddr([from_addr_name, from_addr])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([to_addr_name, to_addr])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "检测到504，官方自考成绩查询入口已关闭"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(host, 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(from_addr, passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(from_addr, [to_addr, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def nextTimeMail(zkzh, nextTime, response):
    ret = True
    try:
        msgtext = '检测到 %s，官方自考成绩查询入口异常，将在 %s 重试' % (str(response), nextTime.strftime(frmt))
        msg = MIMEText(msgtext, 'plain', 'utf-8')
        msg['Subject'] = "检测到 %s，官方自考成绩查询入口异常" % (str(response))  # 邮件的主题，也可以说是标题
        logmsg = fenGe(msgtext)
        
        log(zkzh, logmsg)
        if zkzh != "024920431210":
            to_addr = Students.objects.filter(zkzh=zkzh).values("student_email")[0]["student_email"]
            to_addr_name = Students.objects.filter(zkzh=zkzh).values("student_name")[0]["student_name"]
        elif zkzh == "024920431210":
            to_addr = admin_addr
            to_addr_name = "管理员"
        msg['From'] = formataddr([from_addr_name, from_addr])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([to_addr_name, to_addr])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        server = smtplib.SMTP_SSL(host, 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(from_addr, passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(from_addr, [to_addr, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def Mail(zkzh, code, msg, content):
    if zkzh != "024920431210":
        to_addr = Students.objects.filter(zkzh=zkzh).values("student_email")[0]["student_email"]
        to_addr_name = Students.objects.filter(zkzh=zkzh).values("student_name")[0]["student_name"]
    elif zkzh == "024920431210":
        to_addr = admin_addr
        to_addr_name = "管理员"
    ret = True
    try:
        if msg == "似乎有成绩了":
            msgtext = '<html><p>返回码 %s<br>\n%s详细内容：</p>\n%s\n</html>' % (str(code), msg, content)
            msg = MIMEText(msgtext, 'html', 'utf-8')
        else:
            msgtext = '返回码 %s\n%s详细内容：\n%s' % (str(code), msg, content)
            msg = MIMEText(msgtext, 'plain', 'utf-8')
        logmsg = fenGe(msgtext)
        print(logmsg)
        log(zkzh, logmsg)
        msg['From'] = formataddr(["endless小龙的自考成绩查询系统", from_addr])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([to_addr_name, to_addr])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        if msg == "似乎有成绩了":
            msg['Subject'] = "似乎有成绩了!" % (str(code))  # 邮件的主题，也可以说是标题
        else:
            msg['Subject'] = "返回码 %s" % (str(code))  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(host, 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(from_addr, passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(from_addr, [to_addr, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret