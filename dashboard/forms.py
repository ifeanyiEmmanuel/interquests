
from django import forms
from account.models import AccountUser
from dashboard.models import Dashboard

from . models import Dashboard
from django.utils.translation import gettext_lazy as _
from django.forms import Widget
from djmoney.forms.fields import MoneyField
from djmoney.money import Money

from django.core.exceptions import ValidationError


class DepositForm(forms.ModelForm):
    class Meta:
        model=Dashboard
        fields=['pending_deposit','tokens']
        #widgets={
           # 'pending_deposit':forms.NumberInput(attrs={'class':'form-control','type':'number'}),
           # 'tokens':forms.Select(attrs={'class':'form-control'})
        #}


    def clean_pending_deposit(self,*args,**kwargs):
        instance=self.instance
        user=AccountUser.objects.get(email=instance)
        pending_deposit=self.cleaned_data.get('pending_deposit')
        dash=Dashboard.objects.get(accountUser=user)
        comparator=dash.comparator
        if pending_deposit < comparator:
            raise forms.ValidationError("Minimum deposit is 1 USD")
    
        return pending_deposit

    
  


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields =['wallet_address','tokens','pending_withdrawal']
        widgets={
            'wallet_address':forms.TextInput(attrs={'class':'form-control notice','type':'text',"placeholder":'Enter or paste the address'}),
            'tokens':forms.Select(attrs={'class':'form-control notice'}),
            'pending_withdrwal':forms.NumberInput(attrs={'class':'limit'})
            
            #'network':forms.Select(attrs={'class':'form-control notice'})
    }
      


    
       
       
            


    def clean_pending_withdrawal(self,*args,**kwarags):
        instance=self.instance
        pending_withdrawal= self.cleaned_data.get('pending_withdrawal')
        user=AccountUser.objects.get(email=instance)
        qs =Dashboard.objects.get(accountUser=user)
        profit =qs.profit
        balance = qs.balance + profit
        #balance = balance * 0.90

        if pending_withdrawal > balance:
            raise forms.ValidationError("Insufficient Funds")

        if pending_withdrawal < qs.comparator:
            raise forms.ValidationError("You cannot withdraw less than 1 USD")

        
        return pending_withdrawal

       
class ProfitForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields =['profit']
        widgets={
            'wallet_address':forms.TextInput(attrs={'class':'form-control notice','type':'text',"placeholder":'Enter or paste the address'}),
            'tokens':forms.Select(attrs={'class':'form-control notice'}),
            #'network':forms.Select(attrs={'class':'form-control notice'})
    }

     
class RestrictForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['restriction']
        
        
        


class TransferForm(forms.Form):
    amount = MoneyField()
    #Tn = forms.IntegerField(label="Transfer Number")
    email =forms.EmailField(label='Email address')
    win = forms.IntegerField(label="Wallet Identity Number")
    widgets={
            'amount':forms.NumberInput(attrs={'id':'amount'}),
           
    }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['amount'].widget.attrs.update({'class':'amount form-control','placeholder': '$9000'})
        self.fields['win'].widget.attrs.update({'class':'win form-control','placeholder': '1234567890','maxlength':10})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email address'})
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        minimum = Money(100, 'USD')
        maximum = Money(9000, 'USD')
        if amount < minimum and amount > maximum:
            raise ValidationError("Minimum allowed amount is $100 and maximum allowed amount is $9000")
        
        return amount


    def clean_win(self):
        data = self.cleaned_data['win']
        
        try:
            Dashboard.objects.get(identity_number=data)
            
        except:
            raise ValidationError("Sorry,that doesn't look like a correct wallet number.Please check.")



        

        return data





class PendingTransferForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['pending_transfer']

    




   










       

 