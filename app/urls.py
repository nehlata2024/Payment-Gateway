from django.urls import path
from .views import *
urlpatterns = [
    path("",Home,name="home"),
    path("subscribe/",subscribe,name="subscribe"),
    path('register/',Register,name="register"),
    path('login/',Login,name="login"),
    # path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('cancel/',cancel,name="cancel"),
    path('success/',success,name="success"),
    # path('config/', stripe_config), 
    path('create-payment-link/', create_payment_link, name='create_payment_link'),


]