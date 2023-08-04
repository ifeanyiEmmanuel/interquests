from django.shortcuts import get_object_or_404, render,reverse,redirect
from django.contrib.auth.views import LoginView,PasswordResetView
from django.contrib.auth import login,authenticate
from django.urls import reverse_lazy
from django.views import generic 
from .models import AccountUser
from .forms import AccountCreationForm,LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from dashboard.models import Dashboard
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contents.models import Crypto_logo


class CreateUser(generic.CreateView):
    model = AccountUser
    form_class = AccountCreationForm
    success_url =reverse_lazy('home')
    template_name ="account/register.html"



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Interquests Registration"
        
        return context
    

    
    def form_valid(self, form):
        valid = super(CreateUser,self).form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email,password=password)
        if user is not None:
            login(self.request,user)
            welcome=f"Thank you for joining our program. You are now an offical member of this program.you can now explore your account, and start investing and earning with us, and use all the services that are avaliable for our members" 
           
            messages.success(self.request,welcome)
           

        return valid


        
    def dispatch(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return super(CreateUser,self).dispatch(*args,**kwargs)


  

       
        

    

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = "Login"
        context['logo']=Crypto_logo.objects.all()
        return context
    


    def dispatch(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return super(CustomLoginView,self).dispatch(*args,**kwargs)







