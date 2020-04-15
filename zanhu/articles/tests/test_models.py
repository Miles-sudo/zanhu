from test_plus.test import TestCase
from zanhu.articles.models import Article

from slugify import slugify
from taggit.managers import TaggableManager


class ArticleModelsTest(TestCase):
    def setUp(self) -> None:
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.article = Article.objects.create(
            title="测试文章01",
            user=self.user,
            status="P",
            content="第一篇测试文章",
        )
        self.other_article = Article.objects.create(
            title="测试文章02",
            user=self.other_user,
            # status="P", # 默认为草稿箱 D
            content="第二篇测试文章",
        )

    # 测试__str__方法
    def test_str(self):
        self.assertEqual(self.article.__str__(), "测试文章01")
        self.assertEqual(self.other_article.__str__(), "测试文章02")

    # 测试数据库是否保存slugify
    def test_slug(self):
        self.assertEqual(self.article.slug, slugify(self.article.title))
        self.assertEqual(self.other_article.slug, slugify(self.other_article.title))

    # 判断实例对象是否为Article模型类
    def test_object_isinstance(self):
        assert isinstance(self.article, Article)
        assert isinstance(self.other_article, Article)

    # 测试Article.objects.get_published()
    def test_get_published(self):
        result = Article.objects.get_published()[0]
        assert isinstance(result, Article)
        self.assertEqual(result.title, self.article.title)

    # 测试Article.objects.get_drafts()
    def test_get_drafts(self):
        result = Article.objects.get_drafts()[0]
        assert isinstance(result, Article)
        self.assertEqual(result.title, self.other_article.title)
        self.assertEqual(result.status, "D")


    # 测试Article.objects.get_counted_tags()
    def test_get_counted_tags(self):
        # 参考链接： https://programtalk.com/python-examples/taggit.managers.TaggableManager/
        #           https://programtalk.com/vs2/python/429/django-taggit/tests/tests.py/

        # 为文章添加标签
        self.article.tags.add("test01", "test02")
        self.other_article.tags.add("test02", "test03", "test04")

        # 通过外键查询所有标签，并获取对象的slug值 obj=[<Tag: "test01">,<Tag: "test03">,<Tag: "test04">,<Tag: "test02">]
        got = [getattr(obj, "slug") for obj in Article.tags.all()]
        # 对结果进行排序
        got.sort()
        self.assertListEqual(got, ["test01", "test02", "test03", "test04"])

        # 测试Article.objects.get_counted_tags()
        tags_count_dict = Article.objects.get_counted_tags()
        # 将查询结果 tag_dict.items() 对象 转换为 列表并排序
        result = list(tags_count_dict)
        result.sort()
        assert result == [('test01', 1), ('test02', 2), ('test03', 1), ('test04', 1)]

    # 测试TaggableManager
    def test_TaggableManager(self):
        tm = TaggableManager(help_text="多个标签使用,(英文)隔开", verbose_name="标签")
        ff = tm.formfield()
        # 断言verbose_name
        self.assertEqual(ff.label, "标签")
        self.assertEqual(ff.help_text, "多个标签使用,(英文)隔开")
        # 断言是否必填
        self.assertEqual(ff.required, True)

        # 断言 TaggableManager()是多对多数据表
        self.assertEqual(
            TaggableManager().get_internal_type(), 'ManyToManyField'
        )
