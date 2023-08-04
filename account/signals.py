from django.db.models.signals import post_save
from dashboard.models import Dashboard,WalletInformation
from .models import AccountUser
from django.core.mail import send_mail
from django.contrib.auth import user_logged_in
from django.utils import timezone
from django.conf import settings
from datetime import date
import time
import datetime
from django.core.mail import EmailMultiAlternatives
import random


def create_dashboard(sender,instance,created,**kwargs):
  if created:
    btc = "1H1RBAZQyuAZ2zZtjy8irr7N4otva9vSiS"
    eth = "0x1c886af0d0677acfb2125e10002c771635631fa6"
    usdt = "TKJy7zgfJtChrtPQzsNB3DAJKbH5zkr5Hb"
    bnb = ""
    wallet = random.randrange(2222222222,9999999999)
    WalletInformation.objects.create(user = instance,btc=btc,usdt=usdt,eth=eth)
    Dashboard.objects.create(accountUser=instance,identity_number=wallet)
    print(instance)
    subject = "Congratulations! You have successfully registered on INTERQUESTS"
    text_content = " "
    from_email = "info@interquests.com"
    to_email = instance.email
    if to_email.endswith('@gmail.com'):

      html_content ="""
    <div>
    <p>Congratulations!! you have successfully completed your registration with <strong>INTERQUESTS</strong> trading company.</p>
    <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
    Gmail? <a href="https://contacts.google.com/new">Click here </a>
    </div>
    """
    else:
      html_content ="""
    <div>
    <p>Congratulations!! you have successfully completed your registration with <strong>INTERQUESTS</strong> trading company.</p>"
    <small>We would most likely send subsequent mails to you, we advice that you save our contact so that you wouldn't miss any of our mails</small>
    
    </div>
    """

    msg = EmailMultiAlternatives(subject,text_content, from_email,[to_email])
    msg.attach_alternative(html_content,"text/html")
    #msg.send()
    #theMessage ="Dear ,"+ instance.first_name, +"\n "
   
    
    #send_mail( 'Account creation successful', theMessage, 'info@interquests.com', [instance.email], fail_silently=False, )
    print("email sent successfully")
    print("dashboard created")
  

post_save.connect(create_dashboard,sender=AccountUser)


def update_dashboard(sender,instance,created,**kwargs):
    if created == False:
      btc = "1H1RBAZQyuAZ2zZtjy8irr7N4otva9vSiS"
      eth = "0x1c886af0d0677acfb2125e10002c771635631fa6"
      usdt = "TKJy7zgfJtChrtPQzsNB3DAJKbH5zkr5Hb"
      bnb = ""
      
      Dashboard.objects.get_or_create(accountUser=instance)
     
      WalletInformation.objects.get_or_create(user = instance)
      
      
      
      instance.dashboard.save()
      instance.walletinformation.save()
    
     
      
      print("profile updated")

post_save.connect(update_dashboard,sender=AccountUser)
"""
def notify_login(sender,request,user,**kwargs):
  if user is not None and request.user.is_authenticated:
    year=datetime.date.today().strftime("%Y")
    month=datetime.date.today().strftime("%B")
    day =datetime.date.today().strftime("%A")
    date=datetime.date.today().strftime("%d")

    time=datetime.datetime.now().time()
    now= f'{day},{month} {date}, {year}\n\n\n{time}'
    
    subject='Login Confirmation'
    name=request.user.first_name
    
    message=f"Hello {name},\n\n Please be informed that your digital dashboard was\n accessed on:\n\n\n {now},\n\n You are advised to always keep your login details safe \n\n and never disclose it to anyone. \n\n\n Stay Safe."
    email=request.user.email
    send_mail(subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=False)
    print("email sent")
   

user_logged_in.connect(notify_login,sender=AccountUser)
"""