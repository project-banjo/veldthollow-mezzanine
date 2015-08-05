# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.test import TestCase
from mezzanine.core.models import (
    CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED)
from model_mommy import mommy, recipe
from arrow import Arrow
import fudge

from customizations import views


class BlogRouterViewTest(TestCase):
    def setUp(self):
        self.view = views.BlogRouterView()

    def test_get_category(self):
        request = fudge.Fake()
        mock_blog_views = fudge.Fake().is_a_stub()
        mock_blog_views.blog_post_list.expects_call().with_args(
            request, category='this_slug').returns('category response')

        with fudge.patcher.patched_context(
                views, 'blog_views', mock_blog_views):
            resp = self.view.get(request, slug='this_slug')

        self.assertEqual(resp, 'category response')

    def test_get_post(self):
        request = fudge.Fake()
        mock_blog_views = fudge.Fake().is_a_stub()
        mock_blog_views.blog_post_list.expects_call().with_args(
            request, category='this_slug').raises(Http404)
        mock_blog_views.blog_post_detail.expects_call().with_args(
            request, slug='this_slug').returns('slug response')

        with fudge.patcher.patched_context(
                views, 'blog_views', mock_blog_views):
            resp = self.view.get(request, slug='this_slug')

        self.assertEqual(resp, 'slug response')

    def test_get_404(self):
        pass
        request = fudge.Fake()
        mock_blog_views = fudge.Fake().is_a_stub()
        mock_blog_views.blog_post_list.expects_call().with_args(
            request, category='this_slug').raises(Http404)
        mock_blog_views.blog_post_detail.expects_call().with_args(
            request, slug='this_slug').raises(Http404)

        with fudge.patcher.patched_context(
                views, 'blog_views', mock_blog_views):
            self.assertRaises(
                Http404, self.view.get, request, slug='this_slug')


class HomepageTest(TestCase):
    def setUp(self):
        self.view = views.HomepageView()
        self.post_recipe = recipe.Recipe(
            'blog.BlogPost', status=CONTENT_STATUS_PUBLISHED, expiry_date=None,
            site__id=1)
        self.maxDiff = None

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
            'customizations.User', is_author=True, _quantity=2)
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
