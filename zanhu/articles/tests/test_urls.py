from test_plus.test import TestCase
from django.urls import reverse, resolve


class TestUserURLs(TestCase):
    """将路由函数正向解析，反向解析各一次"""

    def setUp(self):
        self.user = self.make_user("user01")
        self.client.login(username="user01", password="password")

    # 将反向解析
    def test_list_reverse(self):
        # 参数来自self.make_user中创建的测试数据
        self.assertEqual(reverse('articles:list'), '/articles/')

    # 将字符串型的网址解析为路由
    def test_list_resolve(self):
        # 测试函数传递的是类视图
        self.assertEqual(resolve('/articles/').view_name, 'articles:list')
        assert resolve('/articles/').url_name == "list"
        self.assertListEqual(resolve('/articles/').app_names, ["articles"])
        self.assertEqual(resolve('/articles/').namespaces, ["articles"])

    def test_write_new_reverse(self):
        self.assertEqual(reverse('articles:write_new'), '/articles/write-new-article/')

    def test_write_new_resolve(self):
        assert resolve('/articles/write-new-article/').url_name == "write_new"

    @classmethod
    def resolve_name(cls, *url_name, **kwargs):
        p = kwargs
        if not kwargs:
            return resolve('/articles/{}/'.format(url_name)).url_name
        else:
            return reverse('/articles/{}/'.format(url_name), kwargs=p).url_name
            # return resolve('/articles/{}/'.format(url_name), kwargs=kwargs).url_name

    def test_drafts_resolve(self):
        result = resolve('/articles/drafts/').url_name
        assert result == 'drafts'

    def test_drafts_reverse(self):
        self.assertEqual(reverse('articles:drafts'), '/articles/drafts/')

    def test_slug_resolve(self):
        self.assertEqual(resolve("/articles/a_slug/").view_name, "articles:article")

    def test_slug_reverse(self):
        self.assertEqual(reverse('articles:article', kwargs={"slug": "a_slug"}), '/articles/a_slug/')

    #  path("edit/<int:pk>/", views.ArticleEditView.as_view(), name="edit_article"),
    def test_edit_article_resolve(self):
        self.assertEqual(resolve("/articles/edit/1/").view_name, "articles:edit_article")
        self.assertEqual(resolve("/articles/edit/1/").kwargs, {"pk": 1})

    def test_edit_article_reverse(self):
        self.assertEqual(reverse('articles:edit_article', kwargs={"pk": 2333}), '/articles/edit/2333/')
