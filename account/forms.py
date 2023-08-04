import email
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from .models import AccountUser


#custom user create formm
class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AccountUser
        fields = ['email','first_name','last_name','username']



    def clean_email(self):
        email = self.cleaned_data['email']
        if AccountUser.objects.filter(email__iexact=email):
            raise forms.ValidationError('User with this Email Address already exists!!')

        return email.casefold()


    def clean_username(self):
        username = self.cleaned_data['username']
        if AccountUser.objects.filter(username__iexact=username):
            raise forms.ValidationError('User with this Username already exists!!!')
        return username.casefold()


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs.update({"autofocus":True})





    



    
       
        
        
        
       

   

#custom user change formm
class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = AccountUser
        fields = ('first_name','last_name')



class LoginForm(AuthenticationForm):
    class Meta:
        model = AccountUser
        fields = ["email","password"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Email Address','class':'username'})
        self.fields['password'].widget.attrs.update({'placeholder':"*************"})
        
       # self.fields['comment'].widget.attrs.update(size='40')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(username)
        return username.lower()
