from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Problems(models.Model):
    Problem_Name = models.CharField(max_length=50,unique=True)
    Problem_Description=models.TextField() 
    Problem_Tags =models.TextField()
    Problem = models.TextField()
    Problem_Setter = models.CharField(max_length=50)
    Total_submission = models.IntegerField(default=0)
    Total_Accepted = models.IntegerField(default=0)
    Problem_level = models.CharField(max_length=8) 
    Language = models.CharField(max_length=15)
     
    def __str__(self):
        return self.Problem_Name

class Solved(models.Model):
    user_name = models.CharField(max_length=50)
    Problem = models.CharField(max_length=50)
    Date = models.DateTimeField(default = timezone.now)
    Number=models.IntegerField(default=0)
    
    def __str__(self):
        x = self.user_name 
        return x