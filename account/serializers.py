from rest_framework.serializers import ModelSerializer
from .models import AccountUser


class AccountUserSerializer(ModelSerializer):
    class Meta:
        model = AccountUser
        fields = ['email']