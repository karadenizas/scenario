from django import template
from django.db.models import Count
from ..models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

register = template.Library()

@register.inclusion_tag('test.html')
def show_latest_posts(count=30):
    posts = Post.published.all()[:count]

    return {'posts': posts}