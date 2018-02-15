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
     url(r'^reports/$', views.reports,name='reports'),
     url(r'^report_result/(?P<type>[a-z]+)/(?P<subtype>[a-z]+)/$', views.report_result,name='report_result'),
     url(r'^edit_credit/(?P<id>[0-9]+)', views.edit_credit,name='edit_credit'),
     url(r'^delete_credit/(?P<oid>[0-9]+)/', views.delete_credit,name='delete_credit'),
     url(r'^edit_debit/(?P<id>[0-9]+)', views.edit_debit,name='edit_debit'),
     url(r'^delete_debit/(?P<oid>[0-9]+)/', views.delete_debit,name='delete_debit'),
]
