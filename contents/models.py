from contextlib import nullcontext
from distutils.command.upload import upload
from django.db import models


# Create your models here.
class About(models.Model):
    title=models.CharField(max_length=300)
    image=models.ImageField(upload_to="images/",blank=True,null=True)
    content=models.TextField()

    def __str__(self):
        return self.title

class Bounty(models.Model):
    heading=models.CharField(max_length=200)
    sub_heading=models.CharField(max_length=200)
    my_class=models.CharField(max_length=100,blank=True,null=True)
    background_color=models.CharField(max_length=200,blank=True,null=True)


    def __str__(self):
        return self.heading

class Reward(models.Model):
    bounty=models.ForeignKey(Bounty,on_delete=models.CASCADE)
    requirements=models.CharField(max_length=300)
    reward=models.CharField(max_length=200,blank=True,null=True)


    def __str__(self):
        return self.requirements


class Plan(models.Model):
    plan_type=models.CharField(max_length=200)
    
    plan=models.CharField(max_length=200,null=True,blank=True)
    roi=models.PositiveIntegerField(blank=True,null=True)
    Duration=models.CharField(max_length=200,blank=True,null=True)
    Referral=models.IntegerField(null=True,blank=True)
    min_deposit=models.PositiveIntegerField(null=True,blank=True)
    max_deposit=models.PositiveIntegerField(null=True,blank=True)
    withdrawal_period=models.CharField(max_length=300,null=True,blank=False)



    def __str__(self):
        return self.plan


class Crypto_logo(models.Model):
    title=models.CharField(max_length=200)
    svg=models.FileField(upload_to="images/",blank=True,null=True)

    def __str__(self):
        return self.title




class Feedback(models.Model):
    name=models.CharField(max_length=150)
    image=models.ImageField(upload_to="images/")
    testimony=models.TextField(max_length=250)
    country=models.CharField(max_length=250)

    def __str__(self):

        return self.name