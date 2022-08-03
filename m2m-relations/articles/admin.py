from django.contrib import admin

from .models import Article, Tag, ArticleTag
from django.forms import BaseInlineFormSet, ValidationError


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_category = 0
        categories = []
        for form in self.forms:
            if form.cleaned_data.get('tag'):
                if form.cleaned_data.get('tag').name in categories:
                    raise ValidationError('Categories are duplicated')
                else:
                    categories.append(form.cleaned_data.get('tag').name)
            if form.cleaned_data.get('is_main'):
                main_category += 1

        if main_category > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif main_category == 0:
            raise ValidationError('Укажеите основной раздел')

        return super().clean()


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    formset = RelationshipInlineFormset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleTagInline]
