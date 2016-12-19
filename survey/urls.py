from django.conf.urls import url
from django.contrib import admin

from surveyapp.views import CustomerCreateView, SurveyUpdateView, download

urlpatterns = [

    url(r'^$', CustomerCreateView.as_view(), name='newcustomer'),
    url(r'^(?P<pk>[0-9]+)/$', SurveyUpdateView.as_view(), name='survey'),
    url(r'^download/', download, name='download'),
    url(r'^admin/', admin.site.urls, name='admin'),
]
