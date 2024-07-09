from django.shortcuts import render , get_object_or_404
from django.shortcuts import render,redirect,HttpResponse
from .forms import restaurant_form
from django.contrib.auth.models import User
from base.models import restaurants,dish,orders,Images,Reviews
from django.contrib.auth import login ,authenticate,logout
from  django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import aggregates
import random
from .seed import send_mail_to_user_after_order
from .tasks import send_order_mail_to_user_tasks
from accounts.models import UserProfile
from django.db.models import Avg
# Create your views here.

@login_required(login_url="login-page")
def update_restaurant(request,pk):
    restaurant_obj=restaurants.objects.get(id=pk)
    
    if request.method == "POST":
        restaurantName=request.POST.get("restaurantName")
        locations=request.POST.get("locations")
        image=request.FILES.get("image")
        restaurant_obj.restaurantName = restaurantName
        restaurant_obj.locations = locations

        if image:
            restaurant_obj.image = image
        restaurant_obj.save()   
        if img:=request.FILES.get("addimage"):
            image= Images.objects.create(
                restaurant=restaurant_obj,
                image=img   
            )
            image.save()
            return redirect("home")
        return redirect("home")
    
    content={"restaurant":restaurant_obj}
    return render(request,"restaurant/restaurantform.html",content)
@login_required(login_url="login-page")
def delete_restaurant(request,pk):
    restaurant_obj=restaurants.objects.get(id=pk)
    if request.method == "POST":
        restaurant_obj.delete()
        return redirect("home")
    content={"obj":restaurant_obj}
    return render(request,"restaurant/delete_restaurant.html",content)
def restaurant_data(request,pk):
    restaurant=restaurants.objects.get(id=pk)
    q= request.GET.get("q")
    content={}
    review_order = {}
    count_dish = {}
    rating_count={}
    rest_dict={}
    dishes=restaurant.dish_set.all()
    
    for d in dishes:
        avg_review = Reviews.objects.filter(dish=d).aggregate(Avg("review"))['review__avg']
        count_review = Reviews.objects.filter(dish=d).count()
        if d.id not in review_order:
            review_order[d.id] = 0.0
            rating_count[d.id]= 0
        if avg_review is not None:
            review_order[d.id] += float(avg_review)
            rating_count[d.id] += count_review

    try:
        images=restaurant.images_set.all()
        content['images'] = images
    except:
        print(f"{restaurant.restaurantName} have not background image")
    
    create_dish(request,restaurant.id)
    if q is not None :
        try:
            num_q=float(q)
            dishes=dishes.filter(
                                Q(dishName__icontains=q) |
                                Q(description__icontains=q) |
                                Q(price__lte=q)    
                                )
        except Exception:
            dishes=dishes.filter(
                                Q(dishName__icontains=q) |
                                Q(description__icontains=q)    
                                )
    if under_value := request.GET.get('count') is not None:
        dishes=restaurant.dish_set.all()
        dishes=dishes.filter(price__lt=under_value)   
    # content+={}
    content.update({"review_order": review_order,
        "count_dish": count_dish,
        "rating_count":rating_count,
        "dishes":dishes,"restaurant":restaurant})
    return render(request,"restaurant/restaurant_data.html",content)
@login_required(login_url="login-page")
def delete_dish(request,pk):
    dish_obj=dish.objects.get(id=pk)
    restaurant=dish_obj.restaurants
    dish_obj.delete()
    return redirect("restaurant-data",pk=restaurant.id)
@login_required(login_url="login-page")
def update_dish(request,pk):
    dish_obj=dish.objects.get(id=pk)
    dishname=request.POST.get("dishname")
    dish_description=request.POST.get("description")
    dishimage= request.FILES.get("dishImage")  
    price= request.POST.get("price")
    restaurant=dish_obj.restaurants
    if request.method == "POST":
        if dishname :
            dish_obj.dishName=dishname
            dish_obj.description=dish_description
            if dishimage:
                dish_obj.dishImage = dishimage
            dish_obj.price=price    
        dish_obj.save()
        return redirect("restaurant-data",pk=restaurant.id)
    content={"restaurant":restaurant,"dish_obj":dish_obj}
    return render(request,"restaurant/update_dish.html",content)

# def blank(request):
#     # form=user_form()
#     context={"form":form}
#     return render(request,"blank_form.html",context)

def create_dish(request,pk):
    restaurant=restaurants.objects.get(id=pk)
    if request.method == "POST":
        try:
            
            create_dishes=dish.objects.create(
                    dishName=request.POST.get("dishname"),
                    description=request.POST.get("description"),
                    dishImage=request.FILES.get("dishImage"),
                    user=request.user,
                    hotel=restaurant.hotel,
                    restaurants=restaurant,
                    price=request.POST.get("price"),
                    ) 
            
        except Exception as e:
            messages.error(request,e)
        return redirect("restaurant-data",pk=restaurant.id)
    content={"restaurant":restaurant}    
    return render(request,'restaurant/dishform.html',content)
@login_required(login_url="login-page")
def order_dish(request,pk):
    dishe=dish.objects.get(id=pk)
    delavery_charge=int(dishe.price * 0.10)
    total=delavery_charge+(dishe.price * 1.18)
    total=format(total,".2f")
    location=request.POST.get("location")
    rating=Reviews.objects.filter(dish=dishe).aggregate(Avg('review'))['review__avg']
    rating_count=Reviews.objects.filter(dish=dishe).count()
    
    if request.method == "POST":
        if rating:= request.POST.get("rating"):
            comment=request.POST.get("comment") or ''
            review=Reviews.objects.create(
                review=float(rating),
                comment=comment,
                dish=dishe,
                user=request.user
            )
            review.save()
        try:
            order=orders.objects.create(
                delivery_charges=delavery_charge,
                total_charges=(dishe.price+delavery_charge)*1.18,
                location=location,
                restaurants=dishe.restaurants,
                dish=dishe,
                user=request.user
            )
            order.save()
            id=order.id
        
        except Exception as e:
            return redirect("login-page")
        if order:
            try:
            # send_mail_to_user_after_order(id)
                send_order_mail_to_user_tasks.delay(id)
                return redirect("restaurant-data",pk=dishe.restaurants.id )
            except Exception as e:
                print(f"error is : {e}")
    content={"dish":dishe,"delivery":delavery_charge,"total":total,"rating":rating,"rating_count":rating_count}
    return render(request,"restaurant/order_dish.html",content)
        
    
