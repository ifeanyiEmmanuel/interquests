
from django.db import models
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from account.models import AccountUser
from django.db.models.signals import post_save
from django import forms
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator 
from django.core.validators import MinValueValidator, MaxValueValidator
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw 




class Dashboard(models.Model):
  CRYPTO_TOKENS = (
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('USDT','Tether'),
        ('BNB', 'BNB')
    )

  NETWORK = (
        ('BTC', 'BTC'),
        ('TRC20', 'TRC20'),
        ('KCC','KCC'),
        ('ARBITRUM', 'ARBITRUM')
    )



  pending_deposit = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Deposit Amount",default=0.0,  validators=[MinMoneyValidator(0)])
  tokens = models.CharField(max_length=4, choices=CRYPTO_TOKENS,default='ETH')
  comparator= MoneyField(max_digits=14, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="comparator",default=1.0, validators=[MinMoneyValidator(1),MaxMoneyValidator(1)],)
  accountUser = models.OneToOneField(AccountUser,on_delete=models.CASCADE,verbose_name="User",primary_key=True)
  #earnings = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',blank=True,null=True,default=0.0, validators=[MinMoneyValidator(1)])
  balance = MoneyField(max_digits=19, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Balance",default=0.0, validators=[MinMoneyValidator(0)])
  pending_transfer = MoneyField(max_digits=19, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Pending Transfer",default=0.0, validators=[MinMoneyValidator(0)])
  approved_deposit = MoneyField(max_digits=19, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Approved Deposit",default=0.0, validators=[MinMoneyValidator(0)])
  approved_withdrawal = MoneyField(max_digits=19, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Aprroved_withdrawal",default=0.0, validators=[MinMoneyValidator(0)])
  date =models.DateTimeField(auto_now_add=True)

  pending_withdrawal = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Withdrawal Amount",default=0.0, validators=[MinMoneyValidator(0)])
  profit = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Profit",default=0.0, validators=[MinMoneyValidator(0)])
  notification_deposit =models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(1)],null=True,blank=True)
  notification_transfer =models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(1)],null=True,blank=True)
  notification_withdrawal =models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(1)],null=True,blank=True)
  wallet_address=models.CharField(max_length=300,null=True,blank=True)
  restriction = models.BooleanField(default=False,null=False,blank=False)
  identity_number =models.PositiveBigIntegerField(unique=True)
  
  



  def __str__(self):
    return str(self.accountUser)

 





class History(models.Model):
  user=models.ForeignKey(Dashboard,on_delete=models.CASCADE)
  status =models.BooleanField(default=False)
  amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD',blank=True,null=True,verbose_name="Amount",)
  action = models.CharField(max_length=100,verbose_name="Action",null=True,blank=True)
  
  date =models.DateTimeField(auto_now_add=True)


  def __str__(self):
    return str(self.user)






class WalletInformation(models.Model):
  title = models.CharField(max_length=200,default="Wallet address",null=True,blank=True)
  user = models.OneToOneField(AccountUser,on_delete=models.CASCADE,verbose_name="User",primary_key=True)
  btc=models.CharField(max_length=400,verbose_name='Bitcoin',null=True,blank=True)
  eth=models.CharField(max_length=400,verbose_name='Ethereum',null=True,blank=True)
  usdt=models.CharField(max_length=400,verbose_name='Usdt',null=True,blank=True)
  bnb=models.CharField(max_length=400,verbose_name='Bnb',null=True,blank=True)
  logo_btc=models.FileField(blank=True,null=True,upload_to="images/")
  logo_eth=models.FileField(blank=True,null=True,upload_to="images/")
  logo_usdt=models.FileField(blank=True,null=True,upload_to="images/")
  logo_bnb=models.FileField(blank=True,null=True,upload_to="images/")
 
  qr_code_btc=models.ImageField(upload_to="images/",null=True,blank=True)
  qr_code_eth=models.ImageField(upload_to="images/",null=True,blank=True)
  qr_code_usdt=models.ImageField(upload_to="images/",null=True,blank=True)
  qr_code_bnb=models.ImageField(upload_to="images/",null=True,blank=True)

  def __str__(self):
    user = str(self.user)


    
    return  user

  def save(self,*args,**kwargs):
    qrcode_img_eth=qrcode.make(self.eth)
    canvas=Image.new('RGB',(380,380), 'white')
    draw=ImageDraw.Draw(canvas)
    canvas.paste(qrcode_img_eth)
    fname=f"qr_code-{self.eth}.png"
    buffer=BytesIO()
    canvas.save(buffer,'PNG')
    self.qr_code_eth.save(fname,File(buffer),save=False)
    canvas.close()

    qrcode_img_btc=qrcode.make(self.btc)
    canvas_btc=Image.new('RGB',(380,380), 'white')
    draw=ImageDraw.Draw(canvas_btc)
    canvas_btc.paste(qrcode_img_btc)
    fname=f"qr_code-{self.btc}.png"
    buffer=BytesIO()
    canvas_btc.save(buffer,'PNG')
    self.qr_code_btc.save(fname,File(buffer),save=False)
    canvas_btc.close()



    qrcode_img_usdt=qrcode.make(self.usdt)
    canvas_usdt=Image.new('RGB',(380,380), 'white')
    draw=ImageDraw.Draw(canvas_usdt)
    canvas_usdt.paste(qrcode_img_usdt)
    fname=f"qr_code-{self.usdt}.png"
    buffer=BytesIO()
    canvas_usdt.save(buffer,'PNG')
    self.qr_code_usdt.save(fname,File(buffer),save=False)
    canvas_usdt.close()

    
    qrcode_img_bnb=qrcode.make(self.bnb)
    canvas_bnb=Image.new('RGB',(380,380), 'white')
    draw=ImageDraw.Draw(canvas_bnb)
    canvas_bnb.paste(qrcode_img_bnb)
    fname=f"qr_code-{self.bnb}.png"
    buffer=BytesIO()
    canvas_bnb.save(buffer,'PNG')
    self.qr_code_bnb.save(fname,File(buffer),save=False)
    canvas_bnb.close()



    super().save(*args,**kwargs)








  

  