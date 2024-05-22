from .models import *
import stripe
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render, redirect
from .models import SubscriptionPlan
from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
# Create your views here.
def Home(request):
    plans=SubscriptionPlan.objects.all()
    return render(request,"plan.html",{'plans':plans})

# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/subscribe/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + 'cancelled/',
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'name': 'T-shirt',
                    'quantity': 1,
                    'currency': 'usd',
                    'amount': '2000',
                }
            ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request):
    return render(request,'success.html')

def cancel(request):
    return render(request,"cancel.html")

def subscribe(request):
        products=stripe.Product.list()
        print(products)
        return render(request, 'subscribe.html',{'products':products})
    
# def create_payment_link(request):
#     if request.method == 'POST':    
#         product_id = request.POST.get('product_id')
#         print(product_id,"id--------------------------")
#         if product_id:
#             try:
#                 product = stripe.Product.retrieve(product_id)
#                 price_id = stripe.Price.list(product=product_id)
#                 price=price_id.data[0].id
#                 prices=stripe.Price.list()
#                 print(prices,"prices==============================")
#                 user=request.user
#                 print(user.email)
#                 customer=stripe.Customer.retrieve(user.id)
#                 print(customer,"--------------------------------------------------")
#                 if customer is  None:
#                     customer = stripe.Customer.create(
#                         email=request.user.email,
#                         payment_method='pm_card_visa',  # Use a test payment method
#                     )
                
#                 session = stripe.Subscription.create(
                    
#                 customer=customer.id,
#                 items=[
#                     {
#                         'price': price,
#                     },
#                 ],

#                     trial_period_days=15
#                 )
#                 print(session,"-----------------------")
#                 payment_link = session.latest_invoice.hosted_payment_url
#                 print(payment_link,"link=======================")
#                 return redirect(payment_link)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#         else:
#             return JsonResponse({'error': 'Product ID not provided'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)    


def create_payment_link(request):
    if request.method == 'POST':    
        product_id = request.POST.get('product_id')
        print(product_id,"id--------------------------")
        if product_id:
            try:
                product = stripe.Product.retrieve(product_id)
                price_id = stripe.Price.list(product=product_id)
                price=price_id.data[0].id
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price': price,
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='http://127.0.0.1:8000/success/',
                    cancel_url='http://127.0.0.1:8000/subscribe/',
                                subscription_data={
                'trial_period_days': 15
            }
                    # trial_period_days=15
                )
                payment_link = session.url
                return redirect(payment_link)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Product ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)    


def Register(request):
    if request.method=="POST":
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(email)
        user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        print(user)
        login(request,request.user)
        return redirect('subscribe')

    return render(request,"register.html")

def Login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('subscribe')
    return render(request,"login.html")
