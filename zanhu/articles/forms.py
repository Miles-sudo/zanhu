#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Miles__"

from django import forms
from zanhu.articles.models import Article
from markdownx.fields import MarkdownxFormField

'''
很多字段信息是和models.py文件里的模型基本上是一模一样的，
为了避免重复的代码，我们引入了ModelForm，将模型和表单进行绑定
相当于
class ArticleForm(form.Form):
     title=forms.CharField(max_length=32)
     content=forms.IntegerField()
     image=forms.DateField()
     。。。。
'''

class ArticleForm(forms.ModelForm):
    # widget=forms.HiddenInput() 对用户不可见
    title = forms.CharField(widget=forms.HiddenInput())
    # initial = False 初始值 |  required=False 不要求填写
    edited = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)
    content = MarkdownxFormField()

    class Meta:
        model = Article
        # 元数据中定义，可编辑字段
        fields = ["title", "content", "image", "tags", "status", "edited"]
