from django.urls import path
from .views import *

urlpatterns = [
    path('', basket_detail, name='basket_detail'),
    path(r'add/<int:product_id>/', basket_add, name='basket_add'),
    path(r'remove/<int:product_id>/', basket_remove, name='basket_rm')
]