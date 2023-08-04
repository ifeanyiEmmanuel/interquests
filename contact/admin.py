from django.contrib import admin
from django.utils.html import format_html
from .models import Contact
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_filter=["Situation"]
    search_fields=['name','email','subject','Situation']
    list_display=['date','email','subject','status','_']
   
    list_per_page =5

    def _(self,obj):
        if obj.Situation =="Read":
            return True
        else:
            return False
    _.boolean=True

    #function for color

    def status(self,obj):
        if obj.Situation=="Read":
            color='#99c904'
        else:
            color='red'
        return format_html('<strong><p style="color:{}">{}</p></strong>'.format(color,obj.Situation))

    status.allow_tags=True


admin.site.register(Contact,ContactAdmin)
