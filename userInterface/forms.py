from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from snowpenguin.django.recaptcha2.widgets import ReCaptchaHiddenInput


# import models
# from captcha.fields import CaptchaField

class SigninForm(forms.Form):
    zkzh = forms.CharField(min_length=12, max_length=12, widget=forms.TextInput(
        attrs={'class': 'input-material', 'placeholder': '准考证号（12位）', 'data-msg': '请输入12位准考证号'}))
    password = forms.CharField(min_length=16, max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'input-material', 'placeholder': '密码（16位）', 'data-msg': '请输入16位密码'}))
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())
    # captcha = CaptchaField(label='验证码')

    '''
    class Meta:
        model = models.User
        fields = ['name', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, *kwargs)
        self.fields['name'].label = '用户名'
        self.fields['password'].label = '密码'
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})'''


class SignupForm(forms.Form):
    zkzh = forms.CharField(min_length=12, max_length=12, widget=forms.TextInput(
        attrs={'class': 'input-material', 'placeholder': '准考证号（12位）', 'onchange': 'zkzh_change()'}))
    password1 = forms.CharField(min_length=16, max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'input-material', 'placeholder': '密码（16位，稍后会发您邮箱）', 'onchange': 'password1_change()'}))
    password2 = forms.CharField(min_length=16, max_length=16, widget=forms.PasswordInput(
        attrs={'class': 'input-material', 'placeholder': '确认密码', 'onchange': 'password2_change()'}))
    student_name = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'input-material', 'placeholder': '姓名', 'onchange': 'student_name_change()'}))
    student_email = forms.EmailField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-material', 'placeholder': '邮箱', 'onchange': 'student_email_change()'}))
    checkcode = forms.CharField(min_length=18, max_length=18, widget=forms.TextInput(
        attrs={'class': 'input-material', 'placeholder': '邮箱验证码', 'onchange': 'checkcode_change()'}))
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())
    # captcha = CaptchaField(label='验证码')


class ReCaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    # captcha = CaptchaField(label='验证码')


class PasswdResetForm(forms.Form):
    checkcode = forms.CharField(label="邮箱验证码", max_length=18,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱验证码'}))
    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))
    captcha = ReCaptchaField(widget=ReCaptchaHiddenInput())
    # captcha = CaptchaField(label='验证码')
