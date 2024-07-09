from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("base.urls")),
    path("rooms/",include("rooms.urls")),
    path("profile/",include("accounts.urls")),
    path("restaurant-data/",include("restaurant.urls")),
    path("api/",include("api.urls")),
    path("reviews/",include("reviews.urls")),
    path("message/",include("message.urls")),
]   
