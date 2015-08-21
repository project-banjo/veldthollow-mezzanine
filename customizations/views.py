# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, View
from mezzanine.blog import views as blog_views
from mezzanine.blog.models import BlogPost

from customizations.models import Homepage, User


class AuthorArticleListView(ListView):
    model = BlogPost
    template_name = 'blog/author_profile.html'
    context_object_name = 'blog_posts'
    paginate_by = 24

    def get(self, request, *args, **kwargs):
        self.author = self.get_author()
        return super(AuthorArticleListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AuthorArticleListView, self).get_context_data(**kwargs)
        ctx.update(
            author=self.author
        )
        return ctx

    def get_author(self):
        return get_object_or_404(
            User, username=self.kwargs['author'], is_author=True)

    def get_queryset(self):
        qs = super(AuthorArticleListView, self).get_queryset()
        return qs.filter(user=self.author)


class BlogRouterView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.pop('slug')
        try:
            response = blog_views.blog_post_list(
                request, category=slug, *args, **kwargs)
        except Http404:
            response = blog_views.blog_post_detail(
                request, slug=slug, *args, **kwargs)
        return response


class HomepageView(DetailView):
    model = Homepage
    template_name = 'homepage.html'
    latest_article_limit = 3
    featured_article_limit = 6
    featured_category_article_limit = 3
    featured_author_article_limit = 3

    def get_object(self, *args, **kwargs):
        return self.get_queryset().get()

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['latest_articles'] = self.get_latest_articles
        context['featured_category_articles'] = (
            self.get_featured_category_articles)
        context['featured_articles'] = self.get_featured_articles
        context['featured_author_articles'] = self.get_featured_author_articles
        return context

    def get_latest_articles(self):
        return BlogPost.objects.published()[:self.latest_article_limit]

    def get_featured_articles(self):
        return BlogPost.objects.published().filter(featured=True)[
            :self.featured_article_limit]

    def get_featured_category_articles(self):
        return self.object.featured_category.blogposts.published()[
            :self.featured_category_article_limit]

    def get_featured_author_articles(self):
        return self.object.featured_author.blogposts.published()[
            :self.featured_author_article_limit]
