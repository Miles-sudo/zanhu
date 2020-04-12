# import pytest
# from django.test import RequestFactory
#
# from zanhu.users.models import User
# from zanhu.users.views import UserRedirectView, UserUpdateView
#
# pytestmark = pytest.mark.django_db
#
#
# class TestUserUpdateView:
#     """
#     TODO:
#         extracting view initialization code as class-scoped fixture
#         would be great if only pytest-django supported non-function-scoped
#         fixture db access -- this is a work-in-progress for now:
#         https://github.com/pytest-dev/pytest-django/pull/258
#     """
#
#     def test_get_success_url(self, user: User, rf: RequestFactory):
#         view = UserUpdateView()
#         request = rf.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_success_url() == f"/users/{user.username}/"
#
#     def test_get_object(self, user: User, rf: RequestFactory):
#         view = UserUpdateView()
#         request = rf.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_object() == user
#
#
# class TestUserRedirectView:
#     def test_get_redirect_url(self, user: User, rf: RequestFactory):
#         view = UserRedirectView()
#         request = rf.get("/fake-url")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_redirect_url() == f"/users/{user.username}/"

#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Miles__"

from test_plus.test import TestCase
from django.test import RequestFactory
from zanhu.users.views import UserUpdateView

'''
测试view视图韩式，不希望象测试urls一样(相当于通过浏览器，走整个url响应流程，看解析路由能不能找到对应网址)，
走了整个Django请求响应流程，但测试视图并不需要如此，只希望测试视图部分
RequestFactory 提供的不是像浏览器一样的行为，而是提供了一种生成请求实例的方法，该请求实例可用作任何视图的第一个参数。
这意味着您可以像测试任何其他函数一样测试视图函数，就像黑盒一样，使用完全已知的输入来测试特定输出。
文档：https://docs.djangoproject.com/zh-hans/2.2/topics/testing/advanced/#django.test.RequestFactory
'''

class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user()

class TestUpdateView(BaseUserTestCase):
    def setUp(self):
        # 继承父类方法
        super().setUp()
        # 添加测试视图
        self.view = UserUpdateView()
        # 自定义request请求 url任意，不是给url发送请求(url不存在不响应都行) 而是创建请求
        request = self.factory.get('/fake-url')
        # 将当前用户 加入 改次请求中
        request.user = self.user
        # 将该次请求发送给视图
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(),'/users/testuser/')

    def test_get_object(self):
        self.assertEqual(self.view.get_object(),self.user)

    # def test_form_valid(self):
    #     pass

# 其他功能测试等待后续开发完成，发表了个人多少文章，多少问题等待
