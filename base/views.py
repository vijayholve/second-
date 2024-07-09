from django.shortcuts import render,redirect,HttpResponse
from .form import restaurant_form
from django.contrib.auth.models import User
from .models import restaurants,hotel,dish,orders,Images
from django.contrib.auth import login ,authenticate,logout
from  django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import aggregates
import random
from accounts.models import UserProfile
from .seed import register_user_to_send_mail,email_for_otp_verification
from .tasks import send_mail_task
import pygame
def review_user(request):
    review=request.GET.get("rating")
    if request.method == "post":
        
        # pritn("")
        print(review    )
        return HttpResponse(f"{review}") 
    
   
    return HttpResponse(f"hello {review}")
def home(request):
    q=request.GET.get("q") 
    users=User.objects.all()
    images=restaurants.objects.values("image")
    restaurant=restaurants.objects.all()
    if q :   
        restaurant=restaurants.objects.filter(Q(restaurantName__icontains=q) |
                                              Q(locations__icontains=q)) 
        try:
            music=rf"C:\Users\Vijay\django_pro\hotels\media\music\mixkit-retro-game-notification-212.wav"
            pygame.mixer.init()
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()
        except Exception as e:
            print(e)
        
    content={"users":users,"restaurants":restaurant,"dish":dish,"images":images}
    return render(request,"base/home.html",content)
def about(request):
    return render(request,"others/about.html")

def services(request):
    return render(request,"others/services.html")
def conatct(request):   
    return render(request,"others/contact.html")

def login_page(request):
    page="login"
    username=request.POST.get("username")
    password=request.POST.get("password")
    if request.method == "POST":
        try:
            user=User.objects.get(username=username)
        except Exception as e:
            messages.error(request,f"error is {e}")
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("home")
        else :
            messages.error(request,"incorect username and password ")
    context={"page":page}
    return render(request,"base/login_page.html",context)
def register(request):
    page="resister"
    if request.method =="POST":
        return _extracted_from_register_4(request)
    context={"page":page}
    return render(request,"base/login_page.html",context)
# TODO Rename this here and in `register`
def _extracted_from_register_4(request):
    fullname=request.POST.get("fullname")
    email=request.POST.get("email")
    username=request.POST.get("username")
    password=request.POST.get("password")
    confirm_password=request.POST.get("confirm-password")
    print(fullname," ",email," ",username," ",password," ",confirm_password)
    if password != confirm_password :
        messages.error(request,"Password Does Not Matching")
        return redirect("register")
    if username is None or len(username) <  3 :
        messages.error(request,"please enter username")
        return redirect("register")
    if fullname is None or len(fullname) <= 5:
        messages.error(request,"please enter fullname")
        return redirect("register")
    if email is None or len(email) <= 5:
        messages.error(request,"please enter email")
        return redirect("register")
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        if picture:=request.FILES.get("profilePicture"):
            print("Pictrure issaved")
        else:
            picture="images/default.avif"
        profile = UserProfile.objects.create(user=user, profilePicture=picture, dateOfBirth=None)
        profile.save()
        login(request, user)
        send_mail_task.delay(email, fullname)
        return redirect("home")
    except Exception as e:
        print(e)
        messages.error(request, f"error is {e}")
        context = {"page": "register"}
        return render(request, "base/login_page.html", context)

# @login_required(login_url="login-page")
def logout_page(request):
    # user=User.objects.get(id=pk)
    logout(request)
    return redirect("login-page")

@login_required(login_url="login-page ")
def create_restaurant(request):
    hotel_obj=hotel.objects.get(id=3)
    # form=restaurant_form()
    if request.method == "POST":
        restaurantName=request.POST.get("restaurantName")
        locations=request.POST.get("locations")
        image=request.FILES.get("image")
        try:
            restaurant_obj=restaurants.objects.create(
                restaurantName=restaurantName,
                locations=locations,
                image=image,
            hotel=hotel_obj,
            user=request.user
            )
        except Exception as e:
            messages.error(request,e)
        
        restaurant_obj.save()
        images=Images.objects.create(
            restaurant=restaurant_obj,
            image=request.FILES.get("addimage")
        )
        images.save()
        
        return redirect("home")
    # content={"form":form}
    return render(request,"restaurant/restaurantform.html")
# def search_bar(request):
#     if q:=request.GET.get("q"):
#         print(q)
#     return render(request,"base/search_bar.html")