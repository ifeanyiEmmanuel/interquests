
from django.contrib import admin
from .models import Dashboard,History,WalletInformation

# Register your models here.
admin.site.register(Dashboard)

admin.site.register(History)
admin.site.register(WalletInformation)

