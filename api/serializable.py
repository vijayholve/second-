from rest_framework import serializers
from base.models import restaurants,dish
from django.contrib.auth.models import User
from base.models import orders
class serializer_restaurant(serializers.ModelSerializer):
    class Meta:
        model=restaurants
        fields="__all__"
        # depth=1
class User_Serializar(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email']
    
class serializer_dish(serializers.ModelSerializer):
    # user=User_Sesheerializar()
    class Meta:
        model=dish
        fields=["id","dishName","price"]
    def validate_price(self,price):# as you can in the function after the validate add _ and add the column(price) that acces it
        if price < 100:
            raise serializers.ValidationError("Price should be gretter than 100")
        return price
    def validate(self,data):
        speacial="!@#$%^&*()_?"
        if any( c in speacial for c in data["dishName"]):
            raise serializers.ValidationError("speacial character Not allowed")
        return data
class serializer_order(serializers.ModelSerializer):
    class Meta:
        model=orders
        fields="__all__"
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()