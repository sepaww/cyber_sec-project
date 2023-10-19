from django.urls import path

from .views import homePageView, addView, registerView, loginn

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('login/loginn/', loginn, name='add'),
    
    path('login/register/', registerView, name='register'),
]
