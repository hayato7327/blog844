from django.contrib import admin
from django import forms

from . import models


class PostTitleFilter(admin.SimpleListFilter):
    title = '本文'
    parameter_name = 'body_contains'

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(body__icontains=self.value())
        return queryset

    def lookups(self, request, model_admin):
        return [
            ("ブログ", "「ブログ」を含む"),
            ("日記", "「日記」を含む"),
            ("開発", "「開発」を含む"),
        ]


class PostInline(admin.TabularInline):
    model = models.Post
    fields = ('title', 'body')
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class PostAdminForm(forms.ModelForm):
    class Meta:
        labels = {
            'title': 'ブログタイトル'
        }
    
    def clean(self):
        body = self.cleaned_data.get('body')
        if '<h1>' in body:
            raise forms.ValidationError('本文にHTMLタグは使えません。')
        

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    fieldsets = [
        (None, {'fields': ('title', )}),
        ('コンテンツ', {'fields': ('body', )}),
        ('分類', {'fields': ('category', 'tags')}),
        ('メタ', {'fields': ('created', 'updated')})
    ]

    form = PostAdminForm
    filter_horizontal = ('tags',)
        
    
    list_display = ('id', 'title', 'category', 'tags_summary', 'published', 'created', 'updated')
    list_select_related = ('category', )
    list_editable = ('title', 'category')
    search_fields = ('title', 'category__name', 'tags__name', 'created', 'updated')
    ordering = ('-updated', '-created')
    list_filter = (PostTitleFilter, 'category', 'tags', 'created', 'updated')
    
    def tags_summary(self, obj):
        qs = obj.tags.all()
        label = ', '.join(map(str, qs))
        return label
        
    tags_summary.short_description = "tags"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('tags')
        
    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(published=True)
        
    publish.short_description = "公開する"
        
    def unpublish(self, request, queryset):
        queryset.update(published=False)
        
    unpublish.short_description = "下書きに戻す"
    
@admin.register(models.LikeButtonModel)
class LikeButtonModelAdmin(admin.ModelAdmin):
    pass
