from django.shortcuts import render

from articles.models import Article, Tag, ArticleTag
from django.db.models.query import Prefetch


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    tag = request.GET.get('tag')
    tag_list = Tag.objects.all().order_by('name')
    if tag:
        object_list = Article.objects.filter(tag=tag).order_by(ordering).prefetch_related(
            Prefetch('scopes', ArticleTag.objects.order_by('-is_main', 'tag__name')))
    else:
        object_list = Article.objects.order_by(ordering).prefetch_related(
            Prefetch('scopes', ArticleTag.objects.order_by('-is_main', 'tag__name')))

    context = {
        'object_list': object_list,
        'tag_list': tag_list
    }
    return render(request, template, context)
