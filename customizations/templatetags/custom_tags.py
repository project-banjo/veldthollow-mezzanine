from __future__ import unicode_literals
from django.db.models import Count
from mezzanine.blog.models import BlogPost
from mezzanine.generic.models import Keyword
from mezzanine import template

register = template.Library()


@register.as_tag
def blog_keywords(*args):
    """
    Put a list of keywords for blog posts into the template context.
    """
    keyword_ids = BlogPost.objects.published().values_list(
        'keywords__keyword__id', flat=True)
    return Keyword.objects.filter(id__in=set(keyword_ids)).annotate(
        post_count=Count('assignments')).order_by('-post_count')
