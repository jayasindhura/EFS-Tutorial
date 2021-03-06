from django.conf.urls import url
from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'portfolio'
urlpatterns = [
    path('', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_new, name='stock_new'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),

    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/create/', views.investment_new, name='investment_new'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),

    path('fund_list', views.fund_list, name='fund_list'),
    path('fund/create/', views.fund_new, name='fund_new'),
    path('fund/<int:pk>/edit/', views.fund_edit, name='fund_edit'),
    path('fund/<int:pk>/delete/', views.fund_delete, name='fund_delete'),

    path('signup/', views.signup_view, name="signup"),

    path('customer/<int:pk>/portfolio/', views.portfolio, name='portfolio'),
    url('customers_json/', views.CustomerList.as_view()),
    #url(r'^api/customers/$', views.CustomerList),
    url(r'^api/customers/$', views.CustomerList_New),
    url(r'^api/customers/(?P<pk>[0-9]+)$', views.getCustomer),

    url(r'^api/investments/$', views.InvestmentList_New),
    url(r'^api/investments/(?P<pk>[0-9]+)$', views.getInvestment),

    path('pdf/<int:pk>/portfolio/', views.portfolio_summary_pdf,name='portfolio_summary_pdf'),
    path('email/<int:pk>/portfolio/', views.portfolio_summary_pdf_email, name='portfolio_summary_pdf_email'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
