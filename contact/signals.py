from django.db.models.signals import post_save
from contact.models import Contact
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import date
import time
import datetime
from django.core.mail import EmailMultiAlternatives


def send_contact(sender,instance,created,**kwargs):
  if created:
    subject = "Enquiry!!! requires urgent response"
    text_content =instance.email
    from_email = "info@interquests.com"
    to_email = 'contact@interquests.com'
    html_content='<p>Dear Manager,<br> You have a new mail, please attend to it ASAP. <a href="https://interquests.herokuapp.com/admin/contact/contact/">Click here</a> to view.</p>'
    msg = EmailMultiAlternatives(subject,text_content, from_email,[to_email])
    msg.attach_alternative(html_content,"text/html")
    #msg.send()
    print('contact email sent')
    
post_save.connect(send_contact,sender=Contact)
