from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tech.views.tech'),
    url(r'julia', 'tech.views.julia'),
)