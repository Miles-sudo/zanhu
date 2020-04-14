from test_plus.test import TestCase
from django.urls import reverse, resolve


class TestUserURLs(TestCase):
    """将路由函数正向解析，反向解析各一次"""

    def setUp(self):
        self.user = self.make_user("user01")
        self.client.login(username="user01", password="password")

    # 测试views.NewsListView路由
    # 将反向解析news:list
    def test_list_reverse(self):
        # 参数来自self.make_user中创建的测试数据
        self.assertEqual(reverse('news:list'), '/news/')

    # 将字符串型的网址解析为路由
    def test_list_resolve(self):
        # 测试函数传递的是类视图，所以加view_name 方法
        self.assertEqual(resolve('/news/').view_name, 'news:list')


    # 测试views.NewsDeleteView路由
    def test_delete_reverse(self):
        self.assertEqual(reverse('news:delete_news', kwargs={'pk': '1'}), '/news/delete/1/')

    def test_delete_resolve(self):
        print(resolve('/news/delete/1/'))
        self.assertEqual(resolve('/news/delete/1/').view_name, 'news:delete_news')
        self.assertEqual(resolve('/news/delete/100/').kwargs, {'pk': '100'})
        self.assertEqual(resolve('/news/delete/1000/').url_name, "delete_news")
        self.assertEqual(resolve('/news/delete/10000/').app_names, ['news'])
