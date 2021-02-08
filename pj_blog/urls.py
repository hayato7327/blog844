from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from blog.models import Post

admin.site.site_title = '野村勇斗のブログ 内部管理サイト'
admin.site.site_header = '野村勇斗のブログ 内部管理サイト'
admin.site.index_title = 'メニュー'

index_view = ListView.as_view(template_name="blog/post_list.html", model=Post)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login_required(index_view), name="login"),
    path('blog/', include('blog.urls')),
    path('', include("django.contrib.auth.urls")),
]
