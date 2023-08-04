from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import About,Plan,Bounty


def about(request):
    about =About.objects.all()[:1]
    plans= Plan.objects.all()
    title="About Us"
    template_name="contents/about.html"
    context={"about":about,"plans":plans,"title":title}
    return render(request,template_name,context)


def bounty(request):
    bounties=Bounty.objects.all()
    template_name="contents/bounty.html"
    title="Bounty"
    context={'title':title,"bounties":bounties}
    return render(request,template_name,context)
   



