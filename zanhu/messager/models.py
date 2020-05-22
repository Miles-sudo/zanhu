#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Miles__'


from __future__ import unicode_literals
import uuid

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


@python_2_unicode_compatible
class MessageQuerySet(models.query.QuerySet):

    # 用户聊天记录
    def get_conversation(self, sender, recipient):
        """用户间的私信会话"""

        # A发送给B的消息
        qs_one = self.filter(sender=sender, recipient=recipient).select_related('sender', 'recipient')
        # B发送给A的消息
        qs_two = self.filter(sender=recipient, recipient=sender).select_related('sender', 'recipient')
        return qs_one.union(qs_two).order_by('created_at')  # 取并集后按时间排序

    def get_most_recent_conversation(self, recipient):
        """
        获取最近一次私信互动的用户
        recipient -> 不是username 而是一个用户对象
        """
        try:
            # 当前登录用户发送的消息
            qs_sent = self.filter(sender=recipient).select_related('sender', 'recipient')
            # 当前登录用户接收的消息
            qs_received = self.filter(recipient=recipient).select_related('sender', 'recipient')
            # 最后一条消息
            qs = qs_sent.union(qs_received).latest("created_at")
            if qs.sender == recipient:
                # 如果登录用户有发送消息，返回消息的接收者
                return qs.recipient
            # 否则返回消息的发送者
            return qs.sender
        # 如果 没给任何人发送私信qs_sent = None 或没有人给此用户发送私信qs_received=None 取并集 则报错
        except self.model.DoesNotExist: # 捕获异常
            # 如果模型实例不存在，则返回当前用户
            #  get_user_model() -> Return the User model that is active in this project.
            # 也可以直接使用User模型类
            return get_user_model().objects.get(username=recipient.username)


@python_2_unicode_compatible
class Message(models.Model):
    """用户间私信"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 私信发送者
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',
                               blank=True, null=True, on_delete=models.SET_NULL, verbose_name='发送者')
    # 私信接收者
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages',
                                  blank=True, null=True, on_delete=models.SET_NULL, verbose_name='接受者')
    message = models.TextField(blank=True, null=True, verbose_name='内容')
    # True 为未读 Flase 为已读
    unread = models.BooleanField(default=True, verbose_name='是否未读')

    # 没有updated_at，私信发送之后不能修改或撤回
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')

    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.message

    # 标记为已读
    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
