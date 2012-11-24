from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tweetbribe.views.home', name='home'),
    # url(r'^tweetbribe/', include('tweetbribe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'web.views.bribe.index'),
    url(r'^bribe/$', 'web.views.bribe.index'),
    url(r'^bribe/view/(.*)', 'web.views.bribe.view'),
    url(r'^bribe/track/(.*)', 'web.views.bribe.track'),
    url(r'^bribe/confirm/(.*)', 'web.views.bribe.confirm'),
    url(r'^bribe/donate/(.*)', 'web.views.bribe.donate'),
)
