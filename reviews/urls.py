from django.urls import path
from base.models import Reviews 
from . import views 
urlpatterns = [
    
    path("dish-revies/<str:pk>/",views.reviews_dish,name="reviews-dish"),
]




