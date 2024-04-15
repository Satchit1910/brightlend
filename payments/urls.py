from django.urls import path
from .views import make_payment,get_statement

urlpatterns = [
    path('make-payment/', make_payment, name='make_payment'),
    path('get-statement/', get_statement, name='get_statement'),
]