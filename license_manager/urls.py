from django.urls import path
from .views import generate_license_view

urlpatterns = [
    path('generate/', generate_license_view, name='generate_license'),
]
