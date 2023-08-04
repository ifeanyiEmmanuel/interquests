from django.urls import path
from . import views

urlpatterns=[
    path("faq/",views.index_faq,name="faq"),
    path('POP/',views.proof,name="pop"),
    ]