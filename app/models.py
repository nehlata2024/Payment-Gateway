from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SubscriptionPlan(models.Model):
    name=models.CharField( max_length=50)
    price=models.IntegerField()
    duration_month=models.IntegerField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user=models.OneToOneField(User,  on_delete=models.CASCADE)
    plan=models.ForeignKey("SubscriptionPlan",  on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()




