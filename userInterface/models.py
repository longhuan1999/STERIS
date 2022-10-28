from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Students(models.Model):
    student_id = models.AutoField(primary_key=True, verbose_name='学生id')
    zkzh = models.CharField(max_length=12, verbose_name='准考证号')
    password = models.CharField(max_length=256, verbose_name='密码')
    student_name = models.CharField(max_length=16, verbose_name='姓名')
    student_email = models.EmailField(verbose_name='邮箱')
    is_exist = models.BooleanField(default=True, verbose_name='是否存在')
    is_subscribe = models.BooleanField(default=False, verbose_name='是否订阅新成绩')
    signup_date = models.DateTimeField(null=True, verbose_name='注册日期')
    last_signin_date = models.DateTimeField(null=True, verbose_name='上一次登陆时间')
    signup_ip = models.CharField(null=True, blank=True, max_length=36, verbose_name='注册IP')
    signup_location = models.CharField(null=True, blank=True, max_length=36, verbose_name='注册位置')
    last_signin_ip = models.CharField(null=True, blank=True, max_length=36, verbose_name='上一次登陆IP')
    priority = models.IntegerField(default=100000, verbose_name='通知优先级')
    cookies = models.CharField(null=True, max_length=256, verbose_name='Cookie')
    cookies_timeout = models.DateTimeField(null=True, verbose_name='Cookie过期时间')
    student_img = models.CharField(max_length=16, verbose_name='学生头像')

    class Meta:
        db_table = 'tb_students'
        verbose_name = '学生表'
        verbose_name_plural = verbose_name
        unique_together = ('student_id', 'zkzh',)

    def __str__(self):
        return str(self.student_id)

    def setCookie(self, cookie):
        self.update(cookies=cookie)
        self.update(cookies_timeout=timezone.now() + datetime.timedelta(minutes=30))

    def cookieIs_timeout(self):
        return self.cookies_timeout < timezone.now()


class Scores(models.Model):
    score_id = models.AutoField(primary_key=True, verbose_name='成绩id')
    zkzh = models.CharField(max_length=12, verbose_name='课程代号')
    kcmc = models.CharField(max_length=20, verbose_name='课程名称')
    cj = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='成绩')
    ksrq = models.CharField(max_length=12, verbose_name='考试日期')
    bz = models.CharField(max_length=12, verbose_name='备注')
    is_subscribed = models.BooleanField(default=False, verbose_name='是否已发送')

    class Meta:
        db_table = 'tb_scores'
        verbose_name = '成绩表'
        verbose_name_plural = verbose_name


class EmailCheckCode(models.Model):
    email = models.EmailField(unique=False)
    checkcode = models.CharField(max_length=18)
    statu = models.PositiveSmallIntegerField(default=0, verbose_name='验证码状态')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    guoqi_data = models.DateTimeField(verbose_name='过期日期')

    def __str__(self):
        return self.email

    def was_guoqi(self):
        return self.guoqi_data < timezone.now()

    class Meta:
        ordering = ["-add_date"]
        verbose_name = "邮箱验证码"
        verbose_name_plural = "邮箱验证码"
