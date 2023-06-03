from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

from django.conf import settings
from django.conf.urls.static import static
from sitenews.views import page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('news/', include('newsline.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'sitenews.views.page_not_found_view'

