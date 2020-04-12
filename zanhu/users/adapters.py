from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

'''
# 查看account应用 : import allauth.account.urls

适配器，用来连接Users应用，与account应用
定义在settings.py中，settings.py又通过.env文件进行配置
AccountAdapter 为False 则不开放注册 也不能登录
SocialAccountAdapter 为False 第三方账号不能注册 也不能登录

更进一步：
将变量"ACCOUNT_ALLOW_REGISTRATION"/"ACCOUNT_ALLOW_REGISTRATION" 分离出来，实现允许登录注册 不允许第三方登录注册
'''
