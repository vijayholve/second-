from django.urls import path 
from . import views
urlpatterns = [
    path("<str:rest_id>/",views.message_home,name="message-home"),
    path("receiver-list/<str:rest_id>/",views.receiver_list,name="receiver-list"),
    path("owner/<int:receiver_id>/<int:sender_id>/<int:rest_id>/",views.restaurant_owner_reply,name="message-owner"),
]
