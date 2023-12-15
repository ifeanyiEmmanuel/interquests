from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['name','subject','email','message','terms']
        


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id':'name'})
        self.fields['terms'].widget.attrs.update({'required':'True','class':'hidden'})



class MessageForm(forms.ModelForm):
    class Meta:
        model=Contact
        #fields=['name','subject','email','message']
        exclude = ['terms']

        


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id':'name'})
        #self.fields['terms'].widget.attrs.update({'required':'True','class':'hidden'})
        