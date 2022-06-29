from django.db import models
from django.utils import timezone
import  datetime
# Create your models here.


class Question(models.Model):
    #id es generado automaticamente
    question_text= models.CharField(max_length=200)
    pub_date= models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_resently(self):
        return self.pub_date >= timezone.now()-datetime.timezone(days=1)




class Choice(models.Model):
    question =models.ForeignKey(Question, on_delete=models.CASCADE)
    choices_text= models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choices_text