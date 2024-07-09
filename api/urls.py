from django.urls import path
from . import views
urlpatterns = [
    path("",views.all_api,name="all-api"),
    path("login/",views.api_login),
    path("restaurants/",views.restaurants_api,name="restaurants-api"),
    path("restaurants/<str:pk>/",views.restaurant_api,name="restaurant-api"),
    path("dishes/",views.dishes_api,name="dishes-api"),
    path("dishes/<str:pk>/",views.dish_api,name="dishes-api"),
    path("user/",views.User_apis,name="user-api"),
    path("user-api/",views.UserAPI.as_view()),
    path("orders-api/",views.OrdersApi.as_view()),

]
