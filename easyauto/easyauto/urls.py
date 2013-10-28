from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'easyauto.views.home', name='home'),
    # url(r'^easyauto/', include('easyauto.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auto$', 'auto.views.auto'),
    url(r'^ryan$', 'views.ryan'),
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^tech/', 'tech.views.tech'),
)
