from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django import forms
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,reverse,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Dashboard,WalletInformation
from account.models import AccountUser
from  requests import Session,Request 
import json 
from .forms import DepositForm, WithdrawForm
from django.db.models import F
from django.utils import timezone
from django.core.mail import send_mail
from datetime import date
import time
import datetime
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from djmoney.money import Money





# Create your views here.

@login_required   
def dashboard(request):
    title="Dashboard"
    today = date.today()
    year = today.year
    
    
  
    data = request.user
    user = get_object_or_404(AccountUser,email =data.email)
    
    obj = get_object_or_404(Dashboard,accountUser=user.id)
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters ={'start':1,'limit':100,'sort':'market_cap','cryptocurrency_type':'all'}
    headers ={'Accepts':'application/json','X-CMC_PRO_API_KEY':'204cd731-3c5a-4fec-8024-c0aeaa0f998b'}
    session = Session()
    session.headers.update(headers)
    res = session.get(url,params=parameters)
    
    deserialized =json.loads(res.text)['data']
    btc_price=json.loads(res.text)['data'][0]['quote']['USD']['price']
    
    
    balance=obj.balance
    

    btc=balance/btc_price
    pending_transfer = obj.pending_transfer

    win = str(obj.identity_number)
    
    context={'obj':obj,
        'user':user,'deserialized':deserialized,'balance':balance,'btc':btc,"title":title,"year":year,"win":win,"pending_transfer":pending_transfer
    }
    template_name = "dashboard/index.html"
    return render(request,template_name,context)


@login_required
def withdraw(request):
    title="Withdraw"
    myUser = get_object_or_404(AccountUser,email=request.user.email)
    
  
    obj = get_object_or_404(Dashboard,accountUser=request.user.id)
    win = str(obj.identity_number)
    if obj.accountUser!=request.user:
        raise Http404
    form = WithdrawForm(request.POST or None,instance=obj)
    if form.is_valid():
        item=form.save(commit=False)
        depo=item.pending_withdrawal
        com=item.comparator
        item.notification_withdrawal=1
        notification=item.notification_withdrawal
        item.save()
       
        form = WithdrawForm()
        text=f"Withdrawal successfully received ,you would be notified the moment it is processed"
        messages.success(request,text)
        
        
        
        
  
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters ={'start':1,'limit':100,'sort':'market_cap','cryptocurrency_type':'all'}
    headers ={'Accepts':'application/json','X-CMC_PRO_API_KEY':'204cd731-3c5a-4fec-8024-c0aeaa0f998b'}
    session = Session()
    session.headers.update(headers)
    res = session.get(url,params=parameters)
    
    deserialized =json.loads(res.text)['data']

    btc_price=json.loads(res.text)['data'][0]['quote']['USD']['price']
    balance=obj.balance
    btc=balance/btc_price

    
    
    
    #deserialized =" "
    template_name ="dashboard/withdraw.html"
    get_obj=get_object_or_404(Dashboard,accountUser=myUser.id)
    pending= get_obj.pending_withdrawal
    balance =get_obj.balance
    wallet_address=obj.wallet_address
    
    profit =get_obj.profit
    total =profit + balance
    approved =get_obj.approved_withdrawal
    Action="Transaction"
    pending_transfer = obj.pending_transfer
    history=get_obj.history_set.exclude(action="Deposit")
    context ={'pending_transfer':pending_transfer,'win':win,'deserialized':deserialized,'form':form,'pending':pending,'approved':approved,'get_obj':get_obj,"Action":Action,"wallet_address":wallet_address,"balance":balance,"history":history,'btc':btc,"title":title,'profit':profit,'total':total}
    return render(request,template_name,context)
   










@login_required
def deposit(request):
    
    myUser = get_object_or_404(AccountUser,email=request.user.email)
    
  
    obj = get_object_or_404(Dashboard,accountUser=request.user.id)
    win = str(obj.identity_number)
    pending_transfer = obj.pending_transfer
    if obj.accountUser!=request.user:
        raise Http404
    form = DepositForm(request.POST or None,instance=obj)
    if form.is_valid():
        item=form.save(commit=False)

    
    

        depo=item.pending_deposit
        com=item.comparator
        item.notification_deposit=1
        year=datetime.date.today().strftime("%Y")
        month=datetime.date.today().strftime("%B")
        day =datetime.date.today().strftime("%A")
        date=datetime.date.today().strftime("%d")

        time=datetime.datetime.now().time()
        now= f'{day},{month} {date}, {year}\n\n\n{time}'
    
        subject='Deposit Initialized'
        name=request.user.first_name
        print(item.tokens)
        item.save()
       
        form = DepositForm()
       
        
        
    wallet = WalletInformation.objects.get(user = request.user.id )
    object_two = get_object_or_404(Dashboard,accountUser=request.user.id)
    wallet_address = wallet.bnb
    wallet_image = wallet.qr_code_bnb
    name = "BNB"

    if object_two.tokens == 'ETH':
        wallet_address = wallet.eth
        wallet_image = wallet.qr_code_eth
        name = "Ethereum"
        context = {"wallet_address":wallet_address,"wallet_image":wallet_image,"name":name}

    elif object_two.tokens == 'BTC':
        wallet_address = wallet.btc
        wallet_image = wallet.qr_code_btc
        name = "Bitcoin"
        context = {"wallet_address":wallet_address,"wallet_image":wallet_image,"name":name}

    elif object_two.tokens == 'USDT':
        wallet_address = wallet.usdt
        wallet_image = wallet.qr_code_usdt
        name = "USDT"
        context = {"wallet_address":wallet_address,"wallet_image":wallet_image,"name":name}
    
    else:
        wallet_address = wallet.bnb
        wallet_image = wallet.qr_code_bnb
        name = "BNB"
        context = {"wallet_address":wallet_address,"wallet_image":wallet_image,"name":name}
    
    
    balance=obj.balance
    win =str(obj.identity_number)   
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters ={'start':1,'limit':100,'sort':'market_cap','cryptocurrency_type':'all'}
    headers ={'Accepts':'application/json','X-CMC_PRO_API_KEY':'204cd731-3c5a-4fec-8024-c0aeaa0f998b'}
    session = Session()
    session.headers.update(headers)
    res = session.get(url,params=parameters)
    
    deserialized =json.loads(res.text)['data']
    btc_price=json.loads(res.text)['data'][0]['quote']['USD']['price']
    balance=obj.balance
    btc=balance/btc_price
    
   
    
    #deserialized =" "
    template_name ="dashboard/deposit.html"
    get_obj=get_object_or_404(Dashboard,accountUser=myUser.id)
    pending= get_obj.pending_deposit 
    history=get_obj.history_set.exclude(action="Withdrawal")
    
    approved =get_obj.approved_deposit
    balance=get_obj.balance
    Action="Transaction"

    

    profit =get_obj.profit
    total = profit + balance


    context ={'pending_transfer':pending_transfer,'win':win,'profit':profit,'total':total,'deserialized':deserialized,'form':form,'pending':pending,'approved':approved,'get_obj':get_obj,"Action":Action,"balance":balance,"history":history,'btc':btc,"wallet_address":wallet_address,"wallet_image":wallet_image,"name":name}
    return render(request,template_name,context)
    




def transactions(request):
    myUser = get_object_or_404(AccountUser,email=request.user.email)
    #address=get_object_or_404(Address)
  
    obj = get_object_or_404(Dashboard,accountUser=request.user.id)
    pending_transfer = obj.pending_transfer
    if obj.accountUser!=request.user:
        raise Http404
    user=AccountUser.objects.get(email=request.user.email)
    get_obj=get_object_or_404(Dashboard,accountUser=user.id)
    history =get_obj.history_set.all()
    balance=obj.balance
    win =str(obj.identity_number)
    template_name="dashboard/transactions.html"
    context={'history':history,"balance":balance,"win":win,'pending_transfer':pending_transfer}
    return render(request,template_name,context)


@login_required
def settings(request):
    myUser = get_object_or_404(AccountUser,email=request.user.email)
    #address=get_object_or_404(Address)
  
    obj = get_object_or_404(Dashboard,accountUser=request.user.id)
    win =str(obj.identity_number)
    pending_transfer = obj.pending_transfer
    if obj.accountUser!=request.user:
        raise Http404

    #myUser = get_object_or_404(AccountUser,email=request.user.email)
    
  
    obj = get_object_or_404(Dashboard,accountUser=request.user.id)
    balance=obj.balance
    context={"balance":balance,'pending_transfer':pending_transfer}
    template_name="dashboard/settings.html"
    return render(request,template_name,context)





from .forms import TransferForm

@login_required
def transfers(request):
    title ="Transfer funds"
    myUser = get_object_or_404(AccountUser,email=request.user.email)
    obj = get_object_or_404(Dashboard,accountUser=request.user.id)
    pending_transfer = obj.pending_transfer
    win =str(obj.identity_number)
    if obj.accountUser!=request.user:
        raise Http404
    
    form = TransferForm(request.POST or None)
    template_name='dashboard/transfers.html'
    context={"form":form,"title":title,'win':win,'pending_transfer':pending_transfer}
    if form.is_valid():
        check_amount =form.cleaned_data['amount']
        if check_amount > obj.balance:
            text_error=f"Dear customer, you have insufficient funds"
            messages.error(request,text_error)
            context={"form":form,"title":title,"text_error":text_error}

        else:
            
        #Tn = form.cleaned_data['Tn']
            amount = form.cleaned_data['amount']
            win = form.cleaned_data['win']
            email = form.cleaned_data['email']
            receiver = get_object_or_404(Dashboard,identity_number=win)
            context={"form":form,"title":title}
            
            if obj.identity_number == receiver.identity_number:
                text_error=f"sender and receiver account cannot reference same interquests user"
                messages.error(request,text_error)
                context={"form":form,"title":title,"text_error":text_error}
            
            
            else:   
                obj.balance=F('balance')-amount
                receiver.pending_transfer =F('pending_transfer')+ amount
                receiver.notification_transfer = 1
                #print(obj.balance)
                #print(receiver.pending_transfer)
                #print(amount)
                obj.save()
                receiver.save()
                sender_history = obj.history_set.create(user=id,status=True,amount=amount,action="Transfer out")
                sender_history.save()
                #receiver_history = receiver.history_set.create(user=id,status=True,amount=amount,action="Transfer in")
                #receiver_history.save()

                form = TransferForm()

                text=f"{amount} is on it's way to {receiver.accountUser.first_name}"
                messages.success(request,text)
                win = str(obj.identity_number)
                context={"form":form,"title":title,"text":text,"win":win}
                subject = "Transaction Notification"
                text_content = " "
                from_email = "info@interquests.com"
                to_email = receiver.accountUser.email
                if to_email.endswith('@gmail.com'):
                    html_content ="""
    <div>
    <p>Dear {}, {} of <strong>INTERQUESTS Account</strong> just sent you {}.</p>
    <p>A transfer of {} from {} is pending, please contact INTERQUESTS to receive payment</p>
    <a href = "mailto: info@interquests.com">Contact</a><br>
    <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
    Gmail? <a href="https://contacts.google.com/new">Click here </a>
    </div>
    """.format(receiver.accountUser.first_name,myUser.first_name,amount,amount,myUser.first_name)
                else:
                    html_content ="""
    <div>
   <p>Dear {}, {} of <strong>INTERQUESTS Account</strong> just sent you {}.</p>
    <p>A transfer of {} from {} is pending, please contact INTERQUESTS to receive payment</p>
    <a href = "mailto: info@interquests.com">Contact</a><br>
    <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
    
    </div>
    """.format(receiver.accountUser.first_name,myUser.first_name,amount,amount,myUser.first_name)   
                msg = EmailMultiAlternatives(subject,text_content, from_email,[to_email])
                msg.attach_alternative(html_content,"text/html")
                #msg.send()


                subject = "Transaction Notification"
                text_content = " "
                from_email = "info@interquests.com"
                to_email = myUser.email
                if to_email.endswith('@gmail.com'):
                    html_content ="""
    <div>
    <p>Hi {},  you just sent {}  to {} of <strong>INTERQUESTS Account</strong></p>
    <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
    Gmail? <a href="https://contacts.google.com/new">Click here </a>
    </div>
    """.format(myUser.first_name,amount,receiver.accountUser.first_name)
                else:
                    html_content ="""
    <div>
    <p>Hi {},  you just sent {}  to {} of <strong>INTERQUESTS Account</strong></p>
    <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
    
    </div>
    """.format(myUser.first_name,amount,receiver.accountUser.first_name)  
                msg = EmailMultiAlternatives(subject,text_content, from_email,[to_email])
                msg.attach_alternative(html_content,"text/html")
                #msg.send()

            
            


       

        
        
    

    
    return render(request,template_name,context)


"""
from rest_framework.decorators import api_view
from account.serializers import AccountUserSerializer
from django.http import JsonResponse

@api_view(['GET'])
def get_users(request):
    users = AccountUser.objects.all()
    serializer = AccountUserSerializer(users, many = True)
    return JsonResponse(serializer.data,safe=False)

"""
