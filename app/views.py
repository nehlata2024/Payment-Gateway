from django.shortcuts import render
from .models import *
# Create your views here.
def Home(request):
    plans=SubscriptionPlan.objects.all()
    return render(request,"plan.html",{'plans':plans})