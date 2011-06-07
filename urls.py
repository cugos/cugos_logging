from django.conf.urls.defaults import *
from django.views.static import serve
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# For use with MODWSGI
# we had to explicity call projectname (cugos_logging)
# when mapping urls to views for this to work
# that took for fucking ever

urlpatterns = patterns('',
    (r'irchello', 'cugos_logging.irc_log_report.views.hello'),
    (r'^$', 'cugos_logging.irc_log_report.views.index_page'),
    (r'^irc/(?P<chan>\w+)/(?P<YEAR>[0-9]{4})-(?P<MONTH>[0-9]{2})-(?P<DAY>[0-9]{2})/$', 'cugos_logging.irc_log_report.views.take_dump'),
    # Static media files
    (r'^media/(.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    # Example:
    # (r'^cugos_logging/', include('cugos_logging.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
