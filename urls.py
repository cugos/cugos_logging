from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'irchello', 'irc_log_report.views.hello'),
    (r'^$', 'irc_log_report.views.index_page'),
    (r'^irc/(?P<chan>\w+)/(?P<YEAR>[0-9]{4})-(?P<MONTH>[0-9]{2})-(?P<DAY>[0-9]{2})/$', 'irc_log_report.views.take_dump'),
    # Example:
    # (r'^cugos_logging/', include('cugos_logging.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
