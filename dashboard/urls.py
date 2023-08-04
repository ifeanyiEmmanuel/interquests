from django.urls import path
from . import views


urlpatterns =[

path('',views.dashboard,name="dashboard"),
path('deposit/',views.deposit,name="deposit"),
path('withdraw/',views.withdraw,name="withdraw"),
path('transactions/',views.transactions,name='transactions'),
path('setttings/',views.settings,name="settings"),
path('transfers/',views.transfers,name="transfers"),
#path('users/',views.get_users,name="users"),

]
