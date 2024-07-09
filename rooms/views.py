from django.shortcuts import render,redirect,get_object_or_404
from .forms import room_form
from base.models import hotel
from  django.contrib import messages
from .models import Room,Booking
from django.contrib.auth.models import User
import re
from .seed import send_mail_to_user_after_booking
from datetime import datetime
from .seed import send_mail_to_user_after_booking
from datetime import datetime
from django.shortcuts import render
from .models import Room, Booking
from .tasks import send_mail_booking_task
from django.db.models import Q
from base.models import Reviews
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
receiver_mail=None
def home_room(request):
    q=request.GET.get("q") if request.GET.get("q") else ''
    rooms= Room.objects.all()
    review_booking = {}
    rating_count={}
    for room in rooms:
        avg_review = Reviews.objects.filter(room=room).aggregate(Avg("review"))['review__avg']
        count_review = Reviews.objects.filter(room=room).count()
        if room.id not in review_booking:
            review_booking[room.id] = 0.0
            rating_count[room.id]= 0
        if avg_review is not None:
            review_booking[room.id] += float(avg_review)
            rating_count[room.id] += count_review

    if q is not None:
        try:
            q_num=float(q)
            rooms = Room.objects.filter(Q(roomName__icontains=q) |
                                    Q(user__username__icontains=q) |
                                    Q(location__icontains=q)|                    
                                    Q(price__lte=q_num) |
                                    Q(roomType__icontains=q)
                                    )
        except:
            rooms = Room.objects.filter(Q(roomName__icontains=q) |
                                    Q(user__username__icontains=q) |
                                    Q(location__icontains=q)|                    
                                    Q(roomType__icontains=q)
                                    )
    booked_rooms = []
    for room in rooms:
        bookings = Booking.objects.filter(room=room)
        if bookings.exists():
            booked_rooms.append(room) 
    roomrating={}
    for room in rooms:
        avg_rate=Reviews.objects.filter(room=room).aggregate(Avg('review'))['review__avg']
        
    content = {'rooms': rooms, 'booked_rooms': booked_rooms,
               "review_booking":review_booking, "rating_count":rating_count}
    return render(request, 'room/room_home.html', content)

@login_required(login_url="login-page")
def create_room(request):
    form=room_form()
    if request.method == "POST":
        return _extracted_from_create_room_4(request)
    # print(form)
    content={"form":form}
    return render(request, 'room/create_room_old.html',content)


# TODO Rename this here and in `create_room`
def _extracted_from_create_room_4(request):
    form=room_form(request.POST,request.FILES)
    form.user=request.user

    if form.is_valid():
        room=form.save(commit=False)
        room.user=request.user
        room.save()
        return redirect("home-room")
    return redirect("create-room")
def delete_room(request,pk):
    room=get_object_or_404(Room,pk=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home-room")
    # room.delete()
    return render(request,"restaurant/delete_restaurant.html")
from django.db import IntegrityError
def avalable_check(id,start,end):
    room=Room.objects.get(id=id) 
    bookings=room.booking_set.all()
    for book in bookings:
        if book.start_date >= end and book.end_date <= start:
            return False
    return False

@login_required(login_url="login-page")
def booking_room(request, pk): 
    room = Room.objects.get(id=pk)
    rating=Reviews.objects.filter(room=room).aggregate(Avg('review'))['review__avg']
    rating_count=Reviews.objects.filter(room=room).count()
    
    if request.method == "POST":
        startdate = request.POST.get("startdate")
        enddate = request.POST.get("enddate")

        if startdate and enddate:
            start_datetime = datetime.strptime(startdate, '%Y-%m-%d')
            end_datetime = datetime.strptime(enddate, '%Y-%m-%d')
            duration = (end_datetime - start_datetime).days
            gst = int(((room.price) * 18) / 100)
            total = (room.price + gst) * duration
            # if avalable_check(room.id,start_datetime,end_datetime):
            if review:=request.POST.get("rating"):
                rerviws=Reviews.objects.create(
                   review=float(review),
                   room=room,
                   user=request.user
                   )
                rerviws.save()  
            try:
                book = room.booking_set.create(
                    user=request.user,
                    room=room,
                    start_date=start_datetime,
                    end_date=end_datetime,
                    total_price=total,
                    duration=duration 
                )
                book.save()
                
                receiver_mail=book.user.email
                print(receiver_mail)
                id=book.id
                print(id)
                # send_mail_to_user_after_booking(pk,id)
                send_mail_booking_task.delay( pk,id)
                return redirect("home-room")
            except IntegrityError as e:
                # Handle the IntegrityError, maybe by showing an error message to the user
                pass
            # else:
            #     messages.error(request,f"Rooms is not avalable on {start_datetime} to {end_datetime}")
    # If the request method is not POST or if there was an error in creating the booking, render the form
    content = {"room": room,"rating":rating,"rating_count":rating_count}
    return render(request, "room/booking_form.html", content)

@login_required(login_url="login-page")
def user_booked_data(request,pk):
    room=Room.objects.get(id=pk)
    booked=room.booking_set.all()
    content={"booked":booked}
    return render(request,"room/booking_data.html",content)

    