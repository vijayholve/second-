from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import UserProfile
from rooms.models import Room,Booking 
from base.models import orders    
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Avg
from django.template.defaulttags import register
from base.models import Reviews,restaurants,dish
from django.shortcuts import get_object_or_404
from datetime import datetime, date, timedelta


@login_required(login_url="login-page")
def User_profile_fun(request,pk):
    user=User.objects.get(id=pk)
    restaurant=user.restaurants_set.all()
    bookeds=user.booking_set.all()
    rooms=user.room_set.all()
    orders=user.orders_set.all()
    if user.userprofile:
        profile=user.userprofile
    content={"user":user,"profile":profile,"restaurant":restaurant,"booked":bookeds,
             "rooms":rooms,"orders":orders}
    return render(request,"accounts/userProfile.html",content)
def update_profile(request,pk):
    profile=UserProfile.objects.get(id=pk)
    if request.method == "POST":
        
        return _extracted_from_update_profile_5(request, profile)
    content={"profile":profile}
    return render(request,"accounts/update_profile.html",content)


# TODO Rename this here and in `update_profile`
def _extracted_from_update_profile_5(request, profile):
    username=request.POST.get("username")
    city=request.POST.get("city")
    ProfilePicture=request.FILES.get("image")
    dob=request.POST.get("dob")

    if ProfilePicture:
        profile.profilePicture=ProfilePicture
    if dob:
        profile.dateOfBirth=dob
    profile.city=city
    profile.user.username=username
    profile.save()
    return  redirect("profile",pk=profile.user.id)

def create_profile(request):
    users=User.objects.all()
    if request.method == "POST":
        return _extracted_from_create_profile_6(request, users)
    content={"users":users}
    return render(request,"accounts/createprofile.html",content)    
def _extracted_from_create_profile_6(request,users):
    
    city=request.POST.get("city")
    ProfilePicture=request.FILES.get("image")
    dob=request.POST.get("dob")
    user=request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.profilePicture = ProfilePicture
    profile.dateOfBirth = dob
    profile.city = city
    profile.save()
    return  redirect("profile",pk=profile.user.id)

@login_required(login_url="login-page")
def user_rooms_data(request, pk):
    bookings = Booking.objects.filter(user_id=pk).select_related('room')
    rooms = {booking.room for booking in bookings}
    profile = UserProfile.objects.get(user__id=pk)
    review_booking = {}
    rating_count = {}
    start_dates = {}
    end_dates = {}
    total_price = {}
    duration = {}

    for room in rooms:
        avg_review = Reviews.objects.filter(room=room).aggregate(Avg("review"))['review__avg']
        count_review = Reviews.objects.filter(room=room).count()
        total_price_var = Booking.objects.filter(room=room).aggregate(Sum("total_price"))["total_price__sum"]
        duration_var = Booking.objects.filter(room=room).aggregate(Sum('duration'))["duration__sum"]
        room_bookings = Booking.objects.filter(room=room)
        room_start_dates = []
        room_end_dates = []

        for booking in room_bookings:
            room_start_dates.append(booking.start_date)
            room_end_dates.append(booking.end_date)

        if room.id not in start_dates:
            start_dates[room.id] = room_start_dates
        if room.id not in end_dates:
            end_dates[room.id] = room_end_dates

        if room.id not in duration:
            duration[room.id] = 0
        if duration_var is not None:
            duration[room.id] += duration_var

        if room.id not in total_price:
            total_price[room.id] = 0
        if total_price_var is not None:
            total_price[room.id] += total_price_var

        if room.id not in review_booking:
            review_booking[room.id] = 0.0
            rating_count[room.id] = 0
        if avg_review is not None:
            review_booking[room.id] += float(avg_review)
            rating_count[room.id] += count_review

    context = {
        'rooms': rooms,
        "profile": profile,
        "review_booking": review_booking,
        "rating_count": rating_count,
        "start_dates": start_dates,
        "end_dates": end_dates,
        "total_price": total_price,
        "duration": duration
    }
    return render(request, "room/booking_data.html", context)
@login_required(login_url="login-page")
def user_dish_data(request, pk):
    user = get_object_or_404(User, id=pk)
    order = orders.objects.filter(user=user)
    dishes = {o.dish for o in order}
    total_dish=len(dishes)
    sum_order = {}
    review_order = {}
    count_dish = {}
    rating_count={}
    rest_dict={}
    location_dict={}
    
    for d in dishes:
        avg_review = Reviews.objects.filter(dish=d).aggregate(Avg("review"))['review__avg']
        count_review = Reviews.objects.filter(dish=d).count()
        if d.id not in review_order:
            review_order[d.id] = 0.0
            rating_count[d.id]= 0
        if avg_review is not None:
            review_order[d.id] += float(avg_review)
            rating_count[d.id] += count_review
    for d in dishes:
        restaurant=restaurants.objects.get(dish=d)
        rest_name=restaurant.restaurantName
        if d.id not in rest_dict:
            rest_dict[d.id]= ""
        if rest_name is not None:
            rest_dict[d.id]+=rest_name
    for d in dishes:
        total_charges = order.filter(dish=d).aggregate(Sum('total_charges'))['total_charges__sum']
        if d.id not in sum_order:
            sum_order[d.id] = 0
        if total_charges is not None:
            sum_order[d.id] += float(total_charges)
        if d.id not in count_dish:
            count_dish[d.id] = 0
        count_dish[d.id] = order.filter(dish=d).count()
    
    profile = user.userprofile

    content = {
        "dishes": dishes,
        "profile": profile,
        "sum_order": sum_order,
        "review_order": review_order,
        "count_dish": count_dish,
        "rating_count":rating_count,
        "total_dish":total_dish,
        "rest_dict":rest_dict
    }
    
    return render(request, "restaurant/dishes_data_user.html", content)
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)