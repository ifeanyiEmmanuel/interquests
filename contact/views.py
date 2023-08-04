from email import message
from django.http import HttpResponse
from django.shortcuts import render
from .models import Contact
from .forms import ContactForm
from django.contrib import messages
import json

# Create your views here.

def contact_view(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form=ContactForm(request.POST)
        data={}
        if form.is_valid():
            form.save()
            form=ContactForm()
            #text="Message sent Succefully"
            #messages.success(request,text)
            
            
            data['success']=True
            
            
            return HttpResponse(json.dumps(data),content_type='application/json')
        else:
            data['success']=False
            return HttpResponse(json.dumps(data),content_type='application/json') 
    else:
        form=ContactForm()
        template_name="contact/contact.html"
        context={"form":form}
        return render(request,template_name,context)
    
    
        
        
   
    

