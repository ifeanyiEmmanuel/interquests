from django.test import TestCase
from account.models import AccountUser

# Create your tests here.
class AccountUserTestCase(TestCase):
    def user_is_superuser(self):
        new_user = AccountUser.objects.create(email="ifeanyi@gmail.com",username="adam",password="mypassword123",is_supersuer=True)
        self.assertIs(new_user.user_is_superuser(),False)

