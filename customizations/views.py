from django.views.generic import DetailView
from mezzanine.blog.models import BlogPost

from customizations.models import Homepage


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
