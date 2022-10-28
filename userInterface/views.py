from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from .forms import SigninForm, SignupForm, ReCaptchaForm, PasswdResetForm
from .models import Students, EmailCheckCode
import json, decimal, datetime, dateutil.parser, re, hashlib, random, string, urllib.request, urllib.parse, os, time
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django import forms
from .e_Mail import ipLocationMail, signupMail
from .log import log
from .sentScores import sentScores
frmt = "%Y-%m-%d %H:%M:%S"




# Create your views here.
def index(request):
    url_header = get_url_header(request)
    request.session['visit_from'] = url_header
    if not request.session.get('is_signin', None):
        return redirect('signin')
    path = "static\\manage\\images\\users\\" + request.session.get('student_img', None) + ".png"
    if not os.path.exists(path):
        path_or = "static\\manage\\images\\users_templates\\" + str(random.randint(0,50)) + ".png"
        os.system('copy ' + path_or + ' ' + path)
    myinfo_form = ReCaptchaForm()
    return render(request, 'userInterface/myinfo.html', locals())


def signin(request):
    # return render(request, 'userInterface/signin.html')
    url_header = get_url_header(request)
    sign_from(request, url_header)
    if request.headers.get('x-requested-with') == "XMLHttpRequest":
        signin_form = SigninForm(request.POST)
        signin_form.full_clean()
        if 'captcha' in signin_form._errors:
            message = {"code": 1, "msg": "人机验证失败，请刷新页面重试或联系管理员！"}
        elif 'zkzh' in signin_form._errors or not signin_form.cleaned_data['zkzh'].isdigit():
            message = {"code": 1, "msg": "准考证号填写不规范，请等待几秒后重试！"}
        elif 'password' in signin_form._errors or not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!|@|#|$|%|^|&|*]).{16,17}$', signin_form.cleaned_data['password']):
            message = {"code": 1, "msg": "密码填写不规范，请等待几秒后重试！"}
        if signin_form.is_valid():  # 确保用户名和密码都不为空
            zkzh = signin_form.cleaned_data['zkzh']
            password = signin_form.cleaned_data['password']
            password = hash_code(password)
            try:
                student = Students.objects.get(zkzh=zkzh, is_exist=True)
            except:
                message = {"code": 2, "msg": "信息不存在！"}
                return HttpResponse(json.dumps(message))
            if student.password == password:
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                last_signin_date = Students.objects.filter(zkzh=zkzh).values("last_signin_date")
                if last_signin_date[0]['last_signin_date']:
                    last_signin_date = last_signin_date[0]['last_signin_date'].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    last_signin_date = "第一次登录"
                last_signin_ip = Students.objects.filter(zkzh=zkzh).values("last_signin_ip")[0]['last_signin_ip']
                
                if last_signin_ip:
                    ip_location_get = ip_location(last_signin_ip)
                    if ip_location_get['code'] == 0:
                        request.session['last_signin_location'] = ip_location_get['msg']
                    else:
                        logmsg = fenGe(ip_location_get['msg'])
                        log('admin', logmsg)
                        ret = ipLocationMail(ip_location_get['msg'])
                        if ret:
                            logmsg = fenGe("IP地址归属查询接口异常邮件发送成功")
                            log('admin', logmsg)
                        else:
                            logmsg = fenGe("IP地址归属查询接口异常邮件发送失败")
                            log('admin', logmsg)
                else:
                    last_signin_ip = "第一次登录"
                    last_signin_date = "第一次登录"
                    request.session['last_signin_location'] = "第一次登录"
                request.session['last_signin_date'] = last_signin_date
                request.session['last_signin_ip'] = last_signin_ip
                
                if ip:
                    ip_location_get = ip_location(ip)
                    if ip_location_get['code'] == 0:
                        request.session['now_sigin_location'] = ip_location_get['msg']
                    else:
                        request.session['now_sigin_location'] = "无法获取本次登录位置"
                        logmsg = fenGe(ip_location_get['msg'])
                        log('admin', logmsg)
                        ret = ipLocationMail(ip_location_get['msg'])
                        if ret:
                            logmsg = fenGe("IP地址归属查询接口异常邮件发送成功")
                            log('admin', logmsg)
                        else:
                            logmsg = fenGe("IP地址归属查询接口异常邮件发送失败")
                            log('admin', logmsg)
                else:
                    ip = "无法获取本次登录IP"
                    request.session['now_sigin_location'] = "无法获取本次登录位置"
                request.session['now_sigin_ip'] = ip
                
                Students.objects.filter(zkzh=zkzh).update(last_signin_date=timezone.now(),
                                                          last_signin_ip=ip)
                request.session['is_signin'] = True
                request.session['student_id'] = student.student_id
                request.session['student_zkzh'] = student.zkzh
                request.session['student_name'] = student.student_name
                request.session['student_email'] = student.student_email
                request.session['student_cheak'] = student.password
                signup_date = student.signup_date
                signup_date = signup_date.strftime("%Y-%m-%d %H:%M:%S")
                request.session['signup_date'] = signup_date
                request.session['signup_ip'] = student.signup_ip
                request.session['signup_location'] = student.signup_location
                if student.is_subscribe:
                    request.session['is_subscribe'] = "已订阅"
                else:
                    request.session['is_subscribe'] = "未订阅"
                request.session['student_img'] = student.student_img
                if request.session.get('is_signin', None):
                    return HttpResponse(json.dumps({"code":0, "msg": "登录成功！"}))
                return HttpResponse(json.dumps({"code": 0, "msg": "登录成功！"}))
            else:
                message = {"code": 1, "msg": "密码不正确，请等待几秒后重试！"}
                return HttpResponse(json.dumps(message))
        else:
            return HttpResponse(json.dumps(message))

    signin_form = SigninForm()
    return render(request, 'userInterface/signin.html', locals())


def signup(request):
    # return render(request, 'userInterface/signup.html')
    url_header = get_url_header(request)
    sign_from(request, url_header)

    if request.headers.get('x-requested-with') == "XMLHttpRequest":
        signup_form = SignupForm(request.POST)
        request.session['in_signup'] = True
        signup_form.full_clean()
        if 'captcha' in signup_form._errors:
            message = {"code": 1, "msg": "人机验证失败，请刷新页面重试或联系管理员！"}
        elif 'zkzh' in signup_form._errors or not signup_form.cleaned_data['zkzh'].isdigit():
            message = {"code": 1, "msg": "准考证号填写不规范，请等待几秒后重试！"}
        elif 'password1' in signup_form._errors or not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!|@|#|$|%|^|&|*]).{16,17}$', signup_form.cleaned_data['password1']):
            message = {"code": 1, "msg": "密码填写不规范，请等待几秒后重试！"}
        elif 'password2' in signup_form._errors or not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!|@|#|$|%|^|&|*]).{16,17}$', signup_form.cleaned_data['password2']) or signup_form.cleaned_data['password1'] != signup_form.cleaned_data['password2']:
            message = {"code": 1, "msg": "确认的密码填写不规范，请等待几秒后重试！"}
        request.session['signup_zkzh'] = request.POST.get('zkzh', None)
        request.session['signup_student_name'] = request.POST.get('student_name', None)
        request.session['signup_password1'] = request.POST.get('password1', None)
        request.session['signup_password2'] = request.POST.get('password2', None)
        request.session['signup_student_email'] = request.POST.get('student_email', None)

        if request.session.get('guoqi_time', None):
            guoqi_time = json.loads(request.session['guoqi_time'], object_hook=object_hook)
            left_time = (guoqi_time - timezone.now()).seconds * 10
            if left_time <= 0 or left_time > 600:
                left_time = 0
            request.session['left_time'] = left_time
        else:
            request.session['left_time'] = 0

        if request.POST.get('resent', None) is not None:
            if 'captcha' not in signup_form._errors:
                if request.session.get('left_time', None) == 0:
                    if re.match(r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$',
                                request.POST.get('student_email', None)):
                        same_student_email = Students.objects.filter(student_email=request.POST.get('student_email', None),
                                                                        is_exist=True)
                        if same_student_email:  # 邮箱地址唯一
                            message = {"code": 1, "msg": '该邮箱已被注册，请检查或联系管理员！'}
                            return HttpResponse(json.dumps(message))
                        sendCode(request.POST.get('student_email', None))
                        guoqi_time = timezone.now() + datetime.timedelta(minutes=1)
                        request.session['guoqi_time'] = json.dumps(guoqi_time, cls=MyJSONEncoder)
                        request.session['left_time'] = 600
                        message = {"code": 0, "msg": '邮箱验证码已发送，请注意查收！'}
                        return HttpResponse(json.dumps(message))
                    else:
                        message = {"code": 1, "msg": '请输入正确的邮箱地址！'}
                        return HttpResponse(json.dumps(message))
                else:
                    message = {"code": 1, "msg": '请在%d秒后再试！' % (request.session.get('left_time', 'None')%600)}
                    return HttpResponse(json.dumps(message))
            else:
                return HttpResponse(json.dumps(message))
        if signup_form.is_valid():  # 获取数据
            zkzh = signup_form.cleaned_data['zkzh']
            student_name = signup_form.cleaned_data['student_name']
            password1 = signup_form.cleaned_data['password1']
            password2 = signup_form.cleaned_data['password2']
            student_email = signup_form.cleaned_data['student_email']
            checkcode = signup_form.cleaned_data['checkcode']
            if password1 != password2:  # 判断两次密码是否相同
                message = {"code": 1, "msg": "两次输入的密码不同！"}
                return HttpResponse(json.dumps(message))
            else:
                same_zkzh = Students.objects.filter(zkzh=zkzh, is_exist=True)
                if same_zkzh:  # 用户名唯一
                    message = {"code": 2, "msg": '该准考证号信息已存在，请检查或联系管理员！'}
                    return HttpResponse(json.dumps(message))
                same_student_email = Students.objects.filter(student_email=student_email, is_exist=True)
                if same_student_email:  # 邮箱地址唯一
                    message = {"code": 2, "msg": '该邮箱已被注册，请检查或联系管理员！'}
                    return HttpResponse(json.dumps(message))
                checkcodeGuoqi("", "")
                checkcodeinfo = EmailCheckCode.objects.filter(email=student_email, checkcode=checkcode).values("statu")
                if checkcodeinfo.exists():
                    statu0count = 0
                    statu2count = 0
                    for i in checkcodeinfo:
                        if i["statu"] == 0:
                            statu0count += 1
                        if i["statu"] == 2:
                            statu2count += 1
                    if statu0count == 0:
                        if statu2count > 0:
                            message = {"code": 1, "msg": "邮箱验证码已失效，请等待几秒后重试！"}
                            return HttpResponse(json.dumps(message))
                        message = {"code": 1, "msg": "邮箱验证码错误，请等待几秒后重试！"}
                        return HttpResponse(json.dumps(message))
                    elif statu0count > 1:
                        message = {"code": 2, "msg": "数据表错误，请联系管理员！"}
                        return HttpResponse(json.dumps(message))
                else:
                    message = {"code": 1, "msg": "邮箱验证码错误，请等待几秒后重试！"}
                    return HttpResponse(json.dumps(message))
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                if ip:
                    ip_location_get = ip_location(ip)
                    if ip_location_get['code'] == 0:
                        ip_location_text = ip_location(ip)['msg']
                    else:
                        logmsg = fenGe(ip_location_get['msg'])
                        log('admin', logmsg)
                        ret = ipLocationMail(ip_location_get['msg'])
                        if ret:
                            logmsg = fenGe("IP地址归属查询接口异常邮件发送成功")
                            log('admin', logmsg)
                        else:
                            logmsg = fenGe("IP地址归属查询接口异常邮件发送失败")
                            log('admin', logmsg)
                else:
                    ip_location_text = ""
                num = string.ascii_letters + string.digits
                student_img = zkzh + "_"
                for i in range(18):
                    student_img += random.choice(num)
                student_img = hashlib.md5(student_img.encode('utf-8')).hexdigest()[8:-8]
                same_zkzh = Students.objects.filter(zkzh=zkzh, is_exist=False)
                if same_zkzh:
                    same_zkzh.update(student_name=student_name, student_email=student_email,
                                     password=hash_code(password1), is_exist=True, is_subscribe=False,
                                     signup_date=timezone.now(), signup_ip=ip, last_signin_ip=None,
                                     last_signin_date=None, signup_location = ip_location_text,
                                     student_img = student_img)
                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    signup_info = '<p><strong style="color: black; font-size: 5">欢迎注册endless小龙的自考成绩查询系统！' \
                                  '<br>您的个人信息是：</strong></p><p>姓名：&emsp;&emsp;%s<br>准考证号：&emsp;&emsp;%s<br>' \
                                  '密码：&emsp;&emsp;%s<br>注册时间：&emsp;&emsp;%s<br>注册IP：&emsp;&emsp;%s<br>' \
                                  '注册IP地理信息：&emsp;&emsp;%s</p>'%(student_name, zkzh, password1, time_now, ip,
                                                                 ip_location_text)
                    ret = signupMail(zkzh, signup_info)
                    if ret:
                        logmsg = fenGe("注册信息邮件发送成功")
                        log('admin', logmsg)
                    else:
                        logmsg = fenGe("注册信息邮件发送失败")
                        log('admin', logmsg)
                    del_signup(request)
                    return HttpResponse(json.dumps({"code": 0, "msg": "注册成功！"}))  # 自动跳转到登录页面
                else:
                    # 当一切都OK的情况下，创建新用户
                    new_student = Students()
                    new_student.zkzh = zkzh
                    new_student.student_name = student_name
                    new_student.password = hash_code(password1)
                    new_student.student_email = student_email
                    new_student.checkcode = checkcode
                    new_student.signup_date = timezone.now()
                    new_student.signup_ip = ip
                    new_student.signup_location = ip_location_text
                    new_student.student_img = student_img
                    new_student.save()
                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    signup_info = '<p><strong style="color: black; font-size: 5">欢迎注册endless小龙的自考成绩查询系统！' \
                                  '<br>您的个人信息是：</strong></p><p>姓名：&emsp;&emsp;%s<br>准考证号：&emsp;&emsp;%s<br>' \
                                  '密码：&emsp;&emsp;%s<br>注册时间：&emsp;&emsp;%s<br>注册IP：&emsp;&emsp;%s<br>' \
                                  '注册IP地理信息：&emsp;&emsp;%s</p>' % (student_name, zkzh, password1, time_now, ip,
                                                                   ip_location_text)
                    ret = signupMail(zkzh, signup_info)
                    if ret:
                        logmsg = fenGe("注册信息邮件发送成功")
                        log('admin', logmsg)
                    else:
                        logmsg = fenGe("注册信息邮件发送失败")
                        log('admin', logmsg)
                    del_signup(request)
                    return HttpResponse(json.dumps({"code": 0, "msg": "注册成功！"}))  # 自动跳转到登录页面
        return render(request, 'userInterface/signup.html', locals())
    if request.session.get('in_signup', None):
        if request.session.get('guoqi_time', None):
            guoqi_time = json.loads(request.session['guoqi_time'], object_hook=object_hook)
            left_time = (guoqi_time - timezone.now()).seconds * 10
            if left_time <= 0 or left_time > 600:
                left_time = 0
            request.session['left_time'] = left_time
        else:
            request.session['left_time'] = 0
    else:
        request.session['left_time'] = 999
    signup_form = SignupForm()
    return render(request, 'userInterface/signup.html', locals())


def signout(request):
    if not request.session.get('is_signin', None):
        return redirect('signin')
    request.session.clear()
    return redirect('/')


def account_settings(request):
    url_header = get_url_header(request)
    request.session['visit_from'] = url_header + "/settings"
    if not request.session.get('is_signin', None):
        return redirect('signin')
    return render(request, 'userInterface/settings.html')


def scores(request):
    url_header = get_url_header(request)
    request.session['visit_from'] = url_header + "/scores"
    if not request.session.get('is_signin', None):
        return redirect('signin')
    return render(request, 'userInterface/scores.html')


def user_logs(request):
    url_header = get_url_header(request)
    request.session['visit_from'] = url_header + "/user_logs"
    if not request.session.get('is_signin', None):
        return redirect('signin')
    return render(request, 'userInterface/user_logs.html')


def help(request):
    url_header = get_url_header(request)
    request.session['visit_from'] = url_header + "/help"
    if not request.session.get('is_signin', None):
        return redirect('signin')
    return render(request, 'userInterface/help.html')


def subscribe_change_on(request):
    if not request.session.get('is_signin', None):
        return redirect('signin')
    if request.headers.get('x-requested-with') == "XMLHttpRequest":
        time.sleep(1)
        myinfo_form = ReCaptchaForm(request.POST)
        myinfo_form.full_clean()
        if 'captcha' in myinfo_form._errors:
            message = {"code": 1, "msg": "人机验证失败，请刷新页面重试或联系管理员！"}
            return HttpResponse(json.dumps(message))
        zkzh = request.session.get("student_zkzh")
        try:
            Students.objects.filter(zkzh=zkzh).update(is_subscribe=True)
            message = {"code": 0, "msg": "订阅已开启！"}
            request.session['is_subscribe'] = "已订阅"
            return HttpResponse(json.dumps(message))
        except:
            message = {"code": 2, "msg": "数据库异常，请检查您的信息后重试或联系管理员！"}
            return HttpResponse(json.dumps(message))



def subscribe_change_off(request):
    if not request.session.get('is_signin', None):
        return redirect('signin')
    if request.headers.get('x-requested-with') == "XMLHttpRequest":
        time.sleep(1)
        myinfo_form = ReCaptchaForm(request.POST)
        myinfo_form.full_clean()
        if 'captcha' in myinfo_form._errors:
            message = {"code": 1, "msg": "人机验证失败，请刷新页面重试或联系管理员！"}
            return HttpResponse(json.dumps(message))
        zkzh = request.session.get("student_zkzh")
        try:
            Students.objects.filter(zkzh=zkzh).update(is_subscribe=False)
            message = {"code": 0, "msg": "订阅已关闭！"}
            request.session['is_subscribe'] = "未订阅"
            return HttpResponse(json.dumps(message))
        except:
            message = {"code": 2, "msg": "数据库异常，请检查您的信息后重试或联系管理员！"}
            return HttpResponse(json.dumps(message))


def test(request):
    url_header = get_url_header(request)
    request.session['visit_from'] = url_header + "/help"
    if not request.session.get('is_signin', None):
        return redirect('signin')
    if request.session.get('student_zkzh') != "024920431210":
        return redirect('/')
    return HttpResponse(sentScores())


def bad_request(request, exception, template_name='userInterface/400.html'):
    return render(request, template_name)


def permission_denied(request, exception, template_name='userInterface/403.html'):
    return render(request, template_name)


def page_not_found(request, exception):
    return render(request, 'userInterface/404.html')

def server_error(request):
    return render(request, 'userInterface/500.html')




# 功能模块区
def hash_code(s, salt='steris'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def get_url_header(request):
    if request.is_secure():
        http = "https"
    else:
        http = "http"
    host = request.META['HTTP_HOST']
    return http + "://" + host


def sign_from(request, url_header):
    if request.method == 'GET':
        # 记住来源的url，如果没有则设置为首页
        if not request.session.get('visit_from', None):
            request.session['visit_from'] = url_header
        elif request.session['visit_from'] == url_header + "/login":
            request.session['visit_from'] = url_header
        elif request.session['visit_from'] == url_header + "/signup":
            request.session['visit_from'] = url_header
    if request.session.get('is_signin', None):
        # 登录状态不允许登录和注册。
        if not request.session.get('visit_from', None):
            request.session['visit_from'] = url_header
        elif request.session['visit_from'] == url_header + "/signin":
            request.session['visit_from'] = url_header
        elif request.session['visit_from'] == url_header + "/signup":
            request.session['visit_from'] = url_header
        return redirect(request.session['visit_from'])


def sendCode(email):
    from_email = settings.DEFAULT_FROM_EMAIL
    emailcode = ""
    num = string.ascii_letters + string.digits
    while True:
        for i in range(18):
            emailcode += random.choice(num)
        if checkcodeGuoqi(email, emailcode):  # 将email没有失效的checkcode设为失效，并检查emailcode是否为已存在的且未失效的checkcode
            break
    EmailCheckCode.objects.create(email=email, checkcode=emailcode, statu=0, add_date=timezone.now(),
                                  guoqi_data=timezone.now() + datetime.timedelta(minutes=15))
    subject = '邮箱验证码'
    text_content = '欢迎使用endless小龙的自考成绩查询系统！\n如果不是您本人操作请忽略此邮件即可!\n您的验证码是：' + emailcode
    html_content = '<p><strong style="color: black; font-size: 5">欢迎使用endless小龙的自考成绩查询系统！<br>如果不是您本人操作请' \
                   '忽略此邮件即可!</strong></p><p>您的验证码是：<strong style="color: black; font-size: 10">' + emailcode + \
                   '</strong></p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def checkcodeGuoqi(email, emailcode):
    emailcodeCheck = True
    for i in EmailCheckCode.objects.filter(statu=0).values('email', 'checkcode'):
        Cemail = i["email"]
        checkcode = i["checkcode"]
        for n in EmailCheckCode.objects.filter(email=Cemail, checkcode=checkcode, statu=0).values("id"):
            q = EmailCheckCode.objects.get(id=n["id"])
            if Cemail == email or q.was_guoqi() is True:
                q.statu = 2
                q.save()
            elif q.was_guoqi() is False and emailcode == checkcode:
                emailcodeCheck = False
    return emailcodeCheck


def del_signup(request):
    try:
        request.session['in_signup'] = False
        del request.session['signup_zkzh']
        del request.session['signup_student_name']
        del request.session['signup_password1']
        del request.session['signup_password2']
        del request.session['signup_student_email']
    except:
        pass

def del_signin(request):
    try:
        request.session['is_signin'] = False
        del request.session['student_id']
        del request.session['student_zkzh']
        del request.session['student_name']
        del request.session['student_email']
        del request.session['student_cheak']
    except:
        pass


def ip_location(ip):
    url = 'http://api.k780.com'
    params = {
        'app': 'ip.get',
        'ip': ip,
        'appkey': '55363',
        'sign': 'cad51814a51238205276e77f9bc00f39',
        'format': 'json',
    }
    params = urllib.parse.urlencode(params)

    f = urllib.request.urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    # print content
    a_result = json.loads(nowapi_call)
    if a_result:
        if a_result['success'] != '0':
            return {'code': 0, 'msg': a_result['result']['detailed']}
        else:
            return {'code': 1, 'msg': a_result['msgid'] + ' ' + a_result['msg']}
    else:
        return {'code': 1, 'msg': 'Request nowapi fail.'}


def fenGe(msgtext):
    fenge = "\n"
    fenge += "*" * 30 + timezone.now().strftime(frmt) + "*" * 50 + "\n"
    fenge += msgtext + "\n"
    return fenge


CONVERTERS = {
    'datetime': dateutil.parser.parse,
    'decimal': decimal.Decimal,
}


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return {"val": obj.isoformat(), "_spec_type": "datetime"}
        elif isinstance(obj, (decimal.Decimal,)):
            return {"val": str(obj), "_spec_type": "decimal"}
        else:
            return super().default(obj)


def object_hook(obj):
    _spec_type = obj.get('_spec_type')
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj['val'])
    else:
        raise Exception('Unknown {}'.format(_spec_type))