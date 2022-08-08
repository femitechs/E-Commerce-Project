from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    
    path('process/<int:id>/', views.payment_process, name='process'),
]