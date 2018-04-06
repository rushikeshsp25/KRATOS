from django.conf.urls import url
from . import views
app_name='Expenditure'
urlpatterns = [
     url(r'^$', views.index,name='index'),
     url(r'^login_user/$', views.login_user, name='login_user'),
     url(r'^logout_user/$', views.logout_user, name='logout_user'),
     url(r'^create_new_user/$', views.create_new_user, name='create_new_user'),
     url(r'^issue_money_to_user/$', views.issue_money_to_user, name='issue_money_to_user'),
     url(r'^receive_money_from_user/$', views.receive_money_from_user, name='receive_money_from_user'),
     url(r'^credits/$', views.credits,name='credits'),
     url(r'^debits/$', views.debits,name='debits'),
     url(r'^users/$', views.users,name='users'),
     url(r'^reports/$', views.reports,name='reports'),
     url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete'),
     url(r'^account/$', views.account,name='account'),
     url(r'^add_event/$', views.add_event,name='add_event'),
     url(r'^add_subevent/$', views.add_subevent,name='add_subevent'),
     url(r'^add_system/$', views.add_system,name='add_system'),
     url(r'^add_category/$', views.add_category,name='add_category'),
     url(r'^change_ongoing_event/$', views.change_ongoing_event,name='change_ongoing_event'),
     url(r'^export/csv/(?P<type>[a-z]+)/$', views.export_csv, name='export_csv'),
     url(r'^report_result/(?P<type>[a-z]+)/(?P<subtype>[A-Za-z0-9]+)/$', views.report_result,name='report_result'),
     url(r'^edit_credit/(?P<id>[0-9]+)', views.edit_credit,name='edit_credit'),
     url(r'^delete_credit/(?P<oid>[0-9]+)/', views.delete_credit,name='delete_credit'),
     url(r'^edit_debit/(?P<id>[0-9]+)', views.edit_debit,name='edit_debit'),
     url(r'^delete_debit/(?P<oid>[0-9]+)/', views.delete_debit,name='delete_debit'),

]
