from email import message
from django.db import models
from django.db.models.fields import BooleanField

# Create your models here

SITUATION=(
    ('Read','Read'),
    ('Unread','Unread'),
)

class Contact(models.Model):
    terms=BooleanField("Accepted the terms",default=False)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    Situation=models.CharField(max_length=100,choices=SITUATION,default="Unread")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

