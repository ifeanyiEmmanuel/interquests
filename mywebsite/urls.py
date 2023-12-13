from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from django.contrib.auth import views as auth_views
from account.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _





urlpatterns = [
    path('',views.index,name="home"),
    path('control_panel/',views.admin_dashboard,name="admin_dashboard"),
    path('pending_deposit/<int:id>/',views.admin_detail,name="admin_detail"),
    path('pending_withdrawal/<int:id>/',views.pending_withdrawal,name="pending_withdrawal"),
    #path('profit/',views.investor_earnings,name="profit"),
    path('profit/add/<int:id>/',views.add_profit,name="add"),
    #path('reset/',views.reset,name="reset"),
    path('reset/<int:id>/',views.reset_detail,name="reset_detail"),
    #path('retrict/',views.restrict_withdrawal_list,name="restrict"),
    path('restrict/<int:id>/',views.restrict_withdrawal,name='restrict_withdrawal'),
    #path('pending_transfer/',views.pending_transfer,name='pending_transfer'),
    path('pending_transfer_detail/<int:id>/',views.pending_transfer_detail,name='pending_transfer_detail'),
    path(_('admin/'), admin.site.urls),
    path('accounts/',include('account.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('',include('contents.urls')),
    path('',include("faq.urls")),
    path('contact/',include("contact.urls")),
    path('accounts/login',CustomLoginView.as_view(),name="login"),
    path('messages/',views.custom_message,name="messages"),
    #path('accounts/change-password/',auth_views.PasswordChangeView.as_view(),name="password_change" ),
    #path('accounts/password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    
    



   #path('currencies/', include('currencies.urls')),

    
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns +=  i18n_patterns(
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.index,name="home"),
    path('control_panel/',views.admin_dashboard,name="admin_dashboard"),
    path('pending_deposit/<int:id>/',views.admin_detail,name="admin_detail"),
    path('pending_withdrawal/<int:id>/',views.pending_withdrawal,name="pending_withdrawal"),
    #path('profit/',views.investor_earnings,name="profit"),
    path('profit/add/<int:id>/',views.add_profit,name="add"),
    #path('reset/',views.reset,name="reset"),
    path('reset/<int:id>/',views.reset_detail,name="reset_detail"),
    #path('retrict/',views.restrict_withdrawal_list,name="restrict"),
    path('restrict/<int:id>/',views.restrict_withdrawal,name='restrict_withdrawal'),
    #path('pending_transfer/',views.pending_transfer,name='pending_transfer'),
    path('pending_transfer_detail/<int:id>/',views.pending_transfer_detail,name='pending_transfer_detail'),
    path('accounts/',include('account.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('',include('contents.urls')),
    path('',include("faq.urls")),
    path('contact/',include("contact.urls")),
    path('accounts/login',CustomLoginView.as_view(),name="login"),
    path('messages/',views.custom_message,name="messages"),
    #path('accounts/change-password/',auth_views.PasswordChangeView.as_view(),name="password_change" ),
    #path('accounts/password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]








#path('api-auth/', include('rest_framework.urls')),
    #path('accounts/users/',include("account.api.urls")),
#path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html")),
