
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext as _ 
from django.utils.translation import get_language,activate,gettext
from django.shortcuts import get_object_or_404, render,reverse,get_list_or_404
from django.http import HttpResponse
from requests import Session,Request
from django.contrib.auth.decorators import login_required
from account.models import AccountUser
from dashboard.models import Dashboard
from dashboard.forms import DepositForm,WithdrawForm,ProfitForm,RestrictForm
from django.db.models import F
from django.core.mail import send_mail
from django.conf import settings
from contents.models import About,Crypto_logo,Feedback,Plan
from  requests import Session,Request 
import json
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from contact.models import Contact


def index(request):
    trans=translate(language='fr')
    about=About.objects.all()
    logo=Crypto_logo.objects.all()
    feed=Feedback.objects.all()
    plans=Plan.objects.all()
    title=_("Home")
    """
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters ={'start':1,'limit':30,'sort':'market_cap','cryptocurrency_type':'all'}
    headers ={'Accepts':'application/json','X-CMC_PRO_API_KEY':'204cd731-3c5a-4fec-8024-c0aeaa0f998b'}
    session = Session()
    session.headers.update(headers)
    res = session.get(url,params=parameters)
    
    deserialized =json.loads(res.text)['data']
    """


    

    deserialized=" "
    template_name="homepage.html"
    context={"deserialized":deserialized,"about":about,"title":title,"logo":logo,"feed":feed,"plans":plans,"trans":trans}
    
    return render(request,template_name,context)

def translate(language):
    current_language=get_language()
    try:
        activate(language)
        text = gettext('home')
    finally:
        activate(current_language)
    return text


@login_required
def admin_dashboard(request):
    count = Contact.objects.all().count()
    
    title="Admin Dashboard"
    if request.user.is_authenticated and request.user.is_staff:
        pending_list =Dashboard.objects.all()
        
        template_name="backend.html"
    else:
        return HttpResponseRedirect(reverse('home'))


    context={"pending_list":pending_list,"title":title,"count":count}
    return render(request,template_name,context)
  




@login_required
def admin_detail(request,id):
    title="Confirm Deposit"
    obj = get_object_or_404(Dashboard,accountUser=id)
    
    if request.user.is_authenticated and request.user.is_staff:
    
      
        form =DepositForm(request.POST or None,instance=obj)
        if form.is_valid():
            item=form.save(commit=False)
            amount =form.cleaned_data.get('pending_deposit')
            
            item.pending_deposit=F('pending_deposit')-amount
            item.approved_deposit=F('approved_deposit')+amount
            item.balance=F('balance') + amount
            item.notification_deposit=0
            
    
            item.save(update_fields=['pending_deposit','balance','approved_deposit','notification_deposit'])
            history =obj.history_set.create(user=id,status=True,amount=amount,action="Deposit")
            history.save()
            to_email = AccountUser.objects.get(email=obj.accountUser)
            subject = "Deposit Confirmed"
            text_content = " "
            from_email = "info@interquests.com"
            html_content ="""
            <div>
            <p>Congratulations!! your deposit has been successfully confirmed, completed, and your account has been credited.<br>
            <strong>INTERQUESTS</strong>.</p>
            <p>Check your balance? <a href="https://www.interquests.com/en/dashboard/deposit/" target="_blank">Click here</a> </p> 

            <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
            Gmail? <a href="https://contacts.google.com/new">Click here </a>
            </div>
            """
            msg = EmailMultiAlternatives(subject,text_content, from_email,[to_email])
            msg.attach_alternative(html_content,"text/html")
            #msg.send()
            print('email sent!!')
            print('amount,',amount)
           
           

            form=DepositForm()
            text=f"Withdrawal successfully received ,you would be notified the moment it is processed"
            messages.success(request,text)
    
    button="Deposit"
    button2='Deposit'
    activity="DEPOSIT"           
    context={"obj":obj,"form":form,"button":button,"activity":activity,"title":title,'button2':button2}
    template_name ="detail.html"
        
    
    return render(request,template_name,context)





 
@login_required
def pending_withdrawal(request,id):
    title="Confirm Withdrawal"
    obj = get_object_or_404(Dashboard,accountUser=id)
    if request.user.is_authenticated and request.user.is_staff:
    
      
        form =WithdrawForm(request.POST or None,instance=obj)
        if form.is_valid():
            item=form.save(commit=False)
            amount =form.cleaned_data.get('pending_withdrawal')
            if amount > item.profit:
                item.pending_withdrawal=item.pending_withdrawal-amount
                AP_difference = amount - item.profit
                the_profit= amount - AP_difference
                item.profit=item.profit-the_profit
                item.balance=item.balance-AP_difference
                
                item.approved_withdrawal=F('approved_withdrawal')+amount

                item.save(update_fields=['pending_withdrawal','balance','approved_withdrawal','notification_withdrawal','profit'])
            else:


                item.pending_withdrawal=F('pending_withdrawal')-amount
                item.approved_withdrawal=F('approved_withdrawal')+amount
                item.profit=item.profit - amount
                item.notification_withdrawal=0
                print(item.profit)
    
                item.save(update_fields=['pending_withdrawal','balance','approved_withdrawal','notification_withdrawal','profit'])
            history =obj.history_set.create(user=id,status=True,amount=amount,action="Withdrawal")
            history.save()
            to_email = AccountUser.objects.get(email=obj.accountUser)
            subject = "Withdrawal Confirmed"
            text_content = " "
            from_email = "info@interquests.com"
            html_content ="""
            <div>
            <p>Congratulations!! your withdrawal has been successfully confirmed, completed, and your account has been debited,and sent to the designated wallet address. <br>
            <strong>INTERQUESTS</strong>.</p>
            <p>Check your balance? <a href="https://www.interquests.com/en/dashboard/deposit/" target="_blank">Click here</a> </p> 

            <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
            Gmail? <a href="https://contacts.google.com/new">Click here </a>
            </div>
            """
            msg = EmailMultiAlternatives(subject,text_content, from_email,[to_email])
            msg.attach_alternative(html_content,"text/html")
            #msg.send()
            print('email sent!!')
            print('amount,',amount)
            
           

            form=WithdrawForm()
            text=f"Withdrawal successfully received ,you would be notified the moment it is processed"
            messages.success(request,text)
    
    button="Withdraw"
    activity="WITHDRAWAL"     
    context={"obj":obj,"form":form,"button":button,"activity":activity,"title":title}
    template_name ="detail.html"
        
    
    return render(request,template_name,context)


@login_required
def investor_earnings(request):
    
    
    if request.user.is_authenticated and request.user.is_staff:

        pending_list = Dashboard.objects.all()
        template_name="profit.html"

    else:
        return HttpResponseRedirect(reverse('home'))
   
    context={"pending_list":pending_list}
    return render(request,template_name,context)



@login_required
def add_profit(request,id):
    button="Add"
    button2 = 'Add'
    title="Add Earnings"
    activity ="profit"
    obj = get_object_or_404(Dashboard,accountUser=id)
    if request.user.is_authenticated and request.user.is_staff:
        form=ProfitForm(request.POST or None,instance=obj)
        if form.is_valid():
            item=form.save(commit=False)
            amount=form.cleaned_data.get('profit')
            item.profit=F('profit')+amount
            item.save(update_fields=['profit'])
            form=ProfitForm()
            text=f"Profit added successfullly"
            messages.success(request,text)
        

           
        template_name="add_profit.html"
        
    else:
        return HttpResponseRedirect(reverse('home'))
    context={"form":form,"button":button,"title":title,'button2':button2,"activity":activity,"obj":obj}
   
    return render(request,template_name,context)
   



@login_required
def reset(request):
    title="Reset"
    
    if request.user.is_authenticated and request.user.is_staff:
        pending_list=Dashboard.objects.all()
        template_name="reset.html"
    else:
        return HttpResponseRedirect(reverse('home'))
    
    context={"title":title,"pending_list":pending_list}
    return render(request,template_name,context)



@login_required
def reset_detail(request,id):
    activity = "Reset"
    title="Reset Pending deposit"
    button="Clear"
    button2='Clear'
    obj = get_object_or_404(Dashboard,accountUser=id)
    if request.user.is_authenticated and request.user.is_staff:
        form =DepositForm(request.POST or None,instance=obj)
        if form.is_valid():
            item=form.save(commit=False)
            amount=form.cleaned_data.get('pending_deposit')
            item.pending_deposit=F('pending_deposit')-amount
            item.notification_deposit=0
            item.save(update_fields=['pending_deposit','notification_deposit'])
            text=f"Profit added successfullly"
            messages.success(request,text)
            form =DepositForm()
            #return HttpResponseRedirect(reverse('reset'))
    
            
        template_name="reset-detail.html"
        pass
    else:
        return HttpResponseRedirect(reverse('home'))
    context={"title":title,"form":form,"button":button,"obj":obj,'button2':button2,"activity":activity}
    return render(request,template_name,context)




@login_required
def restrict_withdrawal_list(request):
    title="Restrict"
    if request.user.is_authenticated and request.user.is_staff:
        pending_list=Dashboard.objects.all()
        template_name="restrict-withdraw.html"
    else:
        return HttpResponseRedirect(reverse('home'))
    
    context={"title":title,"pending_list":pending_list}
    return render(request,template_name,context)



@login_required
def restrict_withdrawal(request,id):
    activity = "Restriction"
    button='Restrict'
    button2='Unrestrict'
    title="Restrict Withdrawal"
    obj= get_object_or_404(Dashboard,accountUser=id)
    if request.user.is_authenticated and request.user.is_staff:
        form = RestrictForm(request.POST or None,instance=obj)
        if form.is_valid():
            item=form.save(commit=False)
            item.save(update_fields=['restriction'])
            text=f"confirmed"
            messages.success(request,text)
            #form = RestrictForm()
            #return HttpResponseRedirect(reverse('restrict'))
        template_name='restrict-detail.html'
    else:
        return HttpResponseRedirect(reverse('home'))
    context = {'title':title,'form':form,'obj':obj,'button':button,'button2':button2,"activity":activity}
    return render(request,template_name,context)

    




from dashboard.forms import PendingTransferForm

def pending_transfer(request):
    title="Confirm pending transfer"
    if request.user.is_authenticated and request.user.is_staff:
        pending_list=Dashboard.objects.all()
        template_name="pending_transfer.html"
    else:
        return HttpResponseRedirect(reverse('home'))

    context={"title":title,"pending_list":pending_list}
    return render(request,template_name,context)
    



def pending_transfer_detail(request,id):
    activity = "Transfer Restriction"
    title =" Confirm Pending Transfers "
    button ='Confirm transfer'
    button2 ='Transfer confirmed'
    
    obj= get_object_or_404(Dashboard,accountUser=id)
    if request.user.is_authenticated and request.user.is_staff:
        form = PendingTransferForm(request.POST or None,instance=obj)
        if form.is_valid():
            item = form.save(commit=False)
            amount = form.cleaned_data['pending_transfer']
            item.pending_transfer=F('pending_transfer')-amount
            item.notification_transfer = 0
            item.balance = F('balance')+amount
            item.save(update_fields=['pending_transfer','notification_transfer','balance'])
            history =obj.history_set.create(user=id,status=True,amount=amount,action="Inward Wire Transfer")
            history.save()
            to_email = AccountUser.objects.get(email=obj.accountUser)
            subject = "Inward Wire Transfer"
            text_content = " "
            from_email = "info@interquests.com"
            html_content ="""
            <div>
            <p>Congratulations!! your pending inward wire transfer has been successfully credited to your account.<br>
            <strong>INTERQUESTS</strong>.</p>
            <p>Check your balance? <a href="https://www.interquests.com/en/dashboard/deposit/" target="_blank">Click here</a> </p> 

            <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
            Gmail? <a href="https://contacts.google.com/new">Click here </a>
            </div>
            """
            msg = EmailMultiAlternatives(subject,text_content, from_email,[to_email])
            msg.attach_alternative(html_content,"text/html")
            #msg.send()
            print('email sent!!')
            print('amount,',amount)
           
           

            form=PendingTransferForm()
            text=f"Inward Wire Transfer confirmed,and account credited"
            messages.success(request,text)
            context = {"button":button,'button2':button2,'title':title,'form':form,"obj":obj,"text":text}

            
     
            return HttpResponseRedirect(reverse('pending_transfer'))


        template_name = 'pending_transfer_details.html'
    else:
        return HttpResponseRedirect(reverse('home'))
    context = {"button":button,'button2':button2,'title':title,'form':form,"obj":obj,"activity":activity}
    return render(request,template_name,context)



def custom_message(request):
    template_name ="messages.html"
    inbox = Contact.objects.all()
    count = inbox.count()
    unread = Contact.objects.filter(Situation="Unread").count()
    unread_inbox = Contact.objects.filter(Situation="Unread")
 

   
    print(unread)
    context ={"count":count,"unread":unread,"inbox":inbox,"unread_inbox": unread_inbox}
    return render(request,template_name,context)