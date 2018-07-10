"""neechsoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView
from evolv.views import EvolvLoginView, EvolvLogOutView
from evolv.views import EvolvHomePageView
from evolv.views import ContactListView, ContactDetailsView
from evolv.views import ContactUpdateView, ContactCreateView
from evolv.views import ContactDeleteView, ContactDetailsView
from evolv.views import ExpenseListView, ExpenseListViewYear
from evolv.views import ExpenseUpdateView, ExpenseDeleteView
from evolv.views import StatusUpdateDeleteView, StatusUpdateUpdateView
from evolv.views import NoteListView
import datetime

current_year = datetime.datetime.now().year

urlpatterns = [

	# home page
    url(r'^$', EvolvHomePageView.as_view(), name='evolvHome'),
	
	# logout / login
    url(r'^accounts/login/$', EvolvLoginView.as_view(), name='evolvLogin'),
    url(r'^accounts/logout/$', EvolvLogOutView.as_view(), name='evolvLogout'),
	
	# contact pages
	url(r'^contact/$', ContactListView.as_view(), name='contacts'),
	url(r'^contact/create$', ContactCreateView.as_view(), name='contactCreate'),
	url(r'^contact/update/(?P<pk>[0-9]+)/$', ContactUpdateView.as_view(), name='contactUpdate'),
	url(r'^contact/delete/(?P<pk>[0-9]+)/$', ContactDeleteView.as_view(), name='contactDelete'),
	url(r'^contact/details/(?P<pk>[0-9]+)/$', ContactDetailsView.as_view(), name='contactDetails'),
	url(r'^statusupdate/delete/(?P<pk>[0-9]+)/$', StatusUpdateDeleteView.as_view(), name='statusUpdateDelete'),
	url(r'^statusupdate/update/(?P<pk>[0-9]+)/$', StatusUpdateUpdateView.as_view(), name='statusUpdateUpdate'),
	
	# expense pages
	url(r'^expense/$', ExpenseListView.as_view(), name='expenses'),
	url(r'^expense/currentyear/', RedirectView.as_view(url="/evolv/expense/%s/" % current_year), name='expenseRedirectCurrentYear'),
	url(r'^expense/(?P<year>[0-9]{4})/$', ExpenseListViewYear.as_view(), name='expenses'),
	url(r'^expense/update/(?P<pk>[0-9]+)/$', ExpenseUpdateView.as_view(), name='expenseUpdate'),
	url(r'^expense/delete/(?P<pk>[0-9]+)/$', ExpenseDeleteView.as_view(), name='expenseDelete'),
	
	# notes pages
	url(r'^notes/$', NoteListView.as_view(), name='notes'),
	
]
