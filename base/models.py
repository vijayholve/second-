from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room
from django.utils import timezone


class hotel(models.Model):
    name=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class restaurants(models.Model):
    restaurantName=models.CharField(max_length=200)
    locations=models.CharField(max_length=200)
    image=models.FileField(upload_to="restaurant_images",null="True",blank=True)
    hotel=models.ForeignKey(hotel,on_delete=models.SET_NULL,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.restaurantName
    class Meta:
        ordering=["-id"]
class dish(models.Model):
    dishName=models.CharField(max_length=200)
    description=models.CharField( max_length=200)
    price=models.IntegerField(blank=True,null=True)
    restaurants=models.ForeignKey(restaurants,on_delete=models.SET_NULL,null=True,blank= True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="dishes")
    dishImage=models.FileField(upload_to="images/",max_length=250,null=True,blank=True)
    hotel=models.ForeignKey(hotel,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.dishName
    class Meta:
        ordering=['-id']
class orders(models.Model):
    restaurants=models.ForeignKey(restaurants,on_delete=models.CASCADE)
    dish=models.ForeignKey(dish,on_delete=models.CASCADE,related_name="dish")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=200,default="Kharadi PUNE 14")
    delivery_charges=models.IntegerField(default=50)
    total_charges=models.IntegerField() 
    def  __str__(self):
        return f"{self.restaurants.restaurantName}"
    class Meta:
        ordering=['-id']  
    
class Images(models.Model):
    restaurant=models.ForeignKey(restaurants,on_delete=models.CASCADE,null=True,blank=True)
    dish=models.ForeignKey(dish,on_delete=models.CASCADE,null=True,blank=True)
    image=models.ImageField(upload_to="images/",max_length=250,null=True,blank=True)
    def __str__(self) -> str:
        return self.restaurant.restaurantName

class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    dish=models.ForeignKey(dish,on_delete=models.CASCADE,null=True,blank=True)
    restaurant=models.ForeignKey(restaurants,on_delete=models.CASCADE,null=True,blank=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE,null=True,blank=True)
    review=models.FloatField(default=0,null=True,blank=True)
    comment=models.TextField(max_length=200,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.review}"

        