from mezzanine.blog.models import BlogCategory
from mezzanine.utils.cache import cache_get, cache_set


def categories(request):
    categories = cache_get('site_categories')
    if not categories:
        categories = BlogCategory.objects.all()
        cache_set('site_categories', categories)
    return {'categories': categories}
