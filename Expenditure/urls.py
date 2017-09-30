from django.conf.urls import url
from . import views
app_name='Expenditure'
urlpatterns = [
     url(r'^$', views.index,name='index'),
     url(r'^login_user/$', views.login_user, name='login_user'),
     url(r'^logout_user/$', views.logout_user, name='logout_user'),
     url(r'^create_new_user/$', views.create_new_user, name='create_new_user'),
     url(r'^credits/$', views.credits,name='credits'),
     url(r'^debits/$', views.debits,name='debits'),
     #url(r'^dashboard/$', views.dashboard,name='dashboard'),
     url(r'^reports/$', views.reports,name='reports'),
     url(r'^report_result/(?P<type>[a-z]+)/(?P<subtype>[a-z]+)$', views.report_result,name='report_result'),

]
