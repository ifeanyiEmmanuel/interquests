
from django.urls import path
from . import views
from .views import CreateUser


urlpatterns = [
    path('signup/',CreateUser.as_view(),name="register"),
   
    

]