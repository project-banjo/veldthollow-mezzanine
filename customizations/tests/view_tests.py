# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from arrow import Arrow
from django.http import Http404
from django.test import TestCase
from django.views import generic
from mezzanine.blog.models import BlogPost
from mezzanine.core.models import (
    CONTENT_STATUS_DRAFT,
    CONTENT_STATUS_PUBLISHED,
)
from model_mommy import mommy, recipe
import fudge

from customizations import views
from customizations.models import User


class AuthorArticleListViewTest(TestCase):
    def setUp(self):
        self.view = views.AuthorArticleListView()

    def test_attrs(self):
        self.assertIsInstance(self.view, generic.ListView)
        self.assertEqual(self.view.model, BlogPost)
        self.assertEqual(self.view.template_name, 'blog/author_profile.html')
        self.assertEqual(self.view.context_object_name, 'blog_posts')
        self.assertEqual(self.view.paginate_by, 24)

    @fudge.patch('customizations.views.ListView.get',
                 'customizations.views.AuthorArticleListView.get_author')
    def test_get(self, mock_get, mock_get_author):
        request = fudge.Fake()
        mock_author = fudge.Fake()
        mock_get_author.expects_call().returns(mock_author)
        mock_get.expects_call().with_args(request).returns('fake response')

        resp = self.view.get(request)

        self.assertEqual(resp, 'fake response')
        self.assertEqual(self.view.author, mock_author)

    @fudge.patch('customizations.views.ListView.get_context_data')
    def test_get_context_data(self, mock_get_ctx):
        mock_get_ctx.expects_call().returns({'fake': 'ctx'})
        self.view.author = fudge.Fake()

        ctx = self.view.get_context_data()

        self.assertDictEqual(ctx, {'fake': 'ctx', 'author': self.view.author})

    @fudge.patch('customizations.views.get_object_or_404')
    def test_get_author(self, mock_get_obj):
        mock_user = fudge.Fake()
        self.view.kwargs = {'author': 'jimbob'}
        mock_get_obj.expects_call().with_args(
            User, username='jimbob', author_status__isnull=False).returns(mock_user)

        author = self.view.get_author()

        self.assertEqual(author, mock_user)

    @fudge.patch('customizations.views.ListView.get_queryset')
    def test_get_queryset(self, mock_get_qs):
        self.view.author = fudge.Fake()
        mock_qs = fudge.Fake()
        mock_get_qs.expects_call().returns(mock_qs)
        mock_qs.expects('filter').with_args(user=self.view.author).returns(mock_qs)

        qs = self.view.get_queryset()

        self.assertEqual(qs, mock_qs)


class AuthorListViewTest(TestCase):
    def setUp(self):
        self.view = views.AuthorListView()

    def test_attrs(self):
        self.assertIsInstance(self.view, generic.ListView)
        self.assertEqual(self.view.model, User)
        self.assertEqual(self.view.template_name, 'blog/authors.html')

    @fudge.patch('customizations.views.ListView.get_context_data',
                 'customizations.views.AuthorListView.get_staff',
                 'customizations.views.AuthorListView.get_guests')
    def test_get_context_data(self, mock_get_ctx, mock_staff, mock_guests):
        mock_get_ctx.expects_call().returns({'mock': 'ctx'})
        mock_staff.expects_call().returns(['staff', 'writers'])
        mock_guests.expects_call().returns(['guest', 'authors'])

        ctx = self.view.get_context_data()

        self.assertDictEqual(
            ctx,
            {'mock': 'ctx',
             'staff': ['staff', 'writers'],
             'guests': ['guest', 'authors']})

    @fudge.patch('customizations.views.AuthorListView.get_queryset')
    def test_get_staff(self, mock_get_qs):
        mock_qs = fudge.Fake()
        (mock_get_qs.expects_call().returns_fake()
         .expects('filter').with_args(author_status=User.STAFF).returns(mock_qs))

        qs = self.view.get_staff()

        self.assertEqual(qs, mock_qs)

    @fudge.patch('customizations.views.AuthorListView.get_queryset')
    def test_get_guests(self, mock_get_qs):
        mock_qs = fudge.Fake()
        (mock_get_qs.expects_call().returns_fake()
         .expects('filter').with_args(author_status=User.GUEST).returns(mock_qs))

        qs = self.view.get_guests()

        self.assertEqual(qs, mock_qs)


class BlogRouterViewTest(TestCase):
    def setUp(self):
        self.view = views.BlogRouterView()

    def test_dispatch_category(self):
        request = fudge.Fake()
        mock_blog_views = fudge.Fake().is_a_stub()
        mock_blog_views.blog_post_list.expects_call().with_args(
            request, category='this_slug').returns('category response')

        with fudge.patcher.patched_context(views, 'blog_views', mock_blog_views):
            resp = self.view.dispatch(request, slug='this_slug')

        self.assertEqual(resp, 'category response')

    def test_dispatch_post(self):
        request = fudge.Fake()
        mock_blog_views = fudge.Fake().is_a_stub()
        mock_blog_views.blog_post_list.expects_call().with_args(
            request, category='this_slug').raises(Http404)
        mock_blog_views.blog_post_detail.expects_call().with_args(
            request, slug='this_slug').returns('slug response')

        with fudge.patcher.patched_context(views, 'blog_views', mock_blog_views):
            resp = self.view.dispatch(request, slug='this_slug')

        self.assertEqual(resp, 'slug response')

    def test_dispatch_404(self):
        request = fudge.Fake()
        mock_blog_views = fudge.Fake().is_a_stub()
        mock_blog_views.blog_post_list.expects_call().with_args(
            request, category='this_slug').raises(Http404)
        mock_blog_views.blog_post_detail.expects_call().with_args(
            request, slug='this_slug').raises(Http404)

        with fudge.patcher.patched_context(views, 'blog_views', mock_blog_views):
            self.assertRaises(Http404, self.view.dispatch, request, slug='this_slug')


class HomepageTest(TestCase):
    def setUp(self):
        self.view = views.HomepageView()
        self.post_recipe = recipe.Recipe(
            'blog.BlogPost', status=CONTENT_STATUS_PUBLISHED, expiry_date=None,
            site__id=1)
        self.maxDiff = None

    @fudge.test
    def test_get_object(self):
        self.view.request = fudge.Fake().is_a_stub()
        self.view.request.page.expects('get_content_model').returns('fake model')

        obj = self.view.get_object()

        self.assertEqual(obj, 'fake model')

    def test_get_context_data(self):
        context_fake = fudge.Fake().is_callable()
        context_fake.expects_call().with_args(
            test='args').returns({'test': 'stuff'})

        with fudge.patcher.patched_context(
                views.DetailView, 'get_context_data', context_fake):
            context = self.view.get_context_data(test='args')

        self.assertDictEqual(
            context,
            {'test': 'stuff',
             'latest_articles': self.view.get_latest_articles,
             'featured_category_articles': (
                 self.view.get_featured_category_articles),
             'featured_articles': self.view.get_featured_articles,
             'featured_author_articles': self.view.get_featured_author_articles
             })

    def test_get_latest_articles(self):
        # post1
        self.post_recipe.make(publish_date=Arrow(2015, 2, 4).datetime)
        post2 = self.post_recipe.make(publish_date=Arrow(2015, 3, 1).datetime)
        post3 = self.post_recipe.make(publish_date=Arrow(2015, 4, 11).datetime)
        # post4
        self.post_recipe.make(
            status=CONTENT_STATUS_DRAFT,
            publish_date=Arrow(2015, 4, 7).datetime)
        post5 = self.post_recipe.make(publish_date=Arrow(2015, 3, 22).datetime)

        articles = self.view.get_latest_articles()

        self.assertSequenceEqual(
            articles, [post3, post5, post2])

    def test_get_featured_category_articles(self):
        category1, category2 = mommy.make('blog.BlogCategory', _quantity=2)
        self.view.object = mommy.make(
            'customizations.Homepage', featured_category=category1)
        post1, post2, post3 = self.post_recipe.make(_quantity=3)
        post4 = self.post_recipe.make(status=CONTENT_STATUS_DRAFT)
        post5, post6 = self.post_recipe.make(_quantity=2)
        category1.blogposts.add(post4, post5, post2, post3, post6)
        category2.blogposts.add(post3, post1, post6)

        articles = self.view.get_featured_category_articles()

        self.assertSequenceEqual(
            articles, [post6, post5, post3])

    def test_get_featured_articles(self):
        # post1, post2, post3
        self.post_recipe.make(featured=True, _quantity=3)
        # post4
        self.post_recipe.make(featured=False, _quantity=1)
        post5, post6 = self.post_recipe.make(featured=True, _quantity=2)
        post7, post8 = self.post_recipe.make(featured=False, _quantity=2)
        post9, post10, post11, post12 = self.post_recipe.make(
            featured=True, _quantity=4)

        articles = self.view.get_featured_articles()

        self.assertSequenceEqual(
            articles, [post12, post11, post10, post9, post6, post5])

    def test_get_featured_author(self):
        author1, author2 = mommy.make(
            'customizations.User', author_status=User.STAFF, _quantity=2)
        self.view.object = mommy.make(
            'customizations.Homepage', featured_author=author1)
        post1, post2, post3 = self.post_recipe.make(
            _quantity=3, user=author1)
        # post4
        self.post_recipe.make(
            user=author1, status=CONTENT_STATUS_DRAFT)
        # post5
        self.post_recipe.make(user=author2)
        post6 = self.post_recipe.make(user=author1)

        articles = self.view.get_featured_author_articles()

        self.assertSequenceEqual(
            articles, [post6, post3, post2])
