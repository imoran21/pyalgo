from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'myapp.views.home', name='home'),
    url(r'^algo/', 'myapp.views.algo', name='home'),
    #url(r'^admin/', include(admin.site.urls)),
)
