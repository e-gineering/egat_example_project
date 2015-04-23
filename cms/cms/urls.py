from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^order_manager/', include('order_manager.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
