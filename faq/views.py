from django.shortcuts import render
from .models import Faq,Answer

# Create your views here.
def index_faq(request):
    faq=Faq.objects.all()[:9]


    title="FAQ"
    template_name="faq/index_faq.html"
    context={"title":title,"faq":faq}
    return render(request,template_name,context)


def proof(request):
    template_name="faq/proof.html"
    title="Proof of Payment"
    context={"title":title}
    return render(request,template_name,context)