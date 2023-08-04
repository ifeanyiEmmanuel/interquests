from django.db import models

# Create your models here.
class Faq(models.Model):
    question=models.CharField(max_length=300)
    date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.question


class Answer(models.Model):
    faq=models.ForeignKey(Faq,on_delete=models.CASCADE)
    answer=models.CharField(max_length=800)


    def __str__(self):
        return self.answer

    