from django.urls import path
from .views import apply_loan

urlpatterns = [
    path('apply-loan/', apply_loan, name='apply_loan'),
]