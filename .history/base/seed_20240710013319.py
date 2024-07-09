from faker import Faker
import random
from django.contrib.auth.models import User
from .data import indian_dishes
from django.conf import settings
from django.core.mail import send_mail
from .models import hotel,dish,restaurants
import os,glob

users=User.objects.all() 
user_list=list(users) 

def seed_fun(n):
    for _ in range(n):
        fake=Faker()
        restaurantName1=fake.name()
        location=fake.address()
        restaurant=restaurants.objects.create(
                restaurantName=restaurantName1,
                locations=location,
                hotel=hotel_obj,
                user=random.choice(user_list)
        )
def upload_image_in_restaurants():
    restaurants_obj=restaurants.objects.all()
    files=glob.glob(os.path.join(rf"C:\Users\Vijay\django_pro\hotels\media\restaurant_images","*"))
    for i,restaurant in enumerate(restaurants_obj):
        restaurant.image=files[i]
        restaurant.save()
        
def seed_dish():
    restaurant=restaurants.objects.all()
    for rest in restaurant:
        for indDish in indian_dishes:
            fake=Faker()
            description = fake.paragraph(nb_sentences=3)  # Generate a paragraph with 3 sentences
            dish=rest.dish_set.create(
                dishName=indDish,
                description=description,
                price=random.randint(100,999),
                restaurants=rest,
                user=random.choice(user_list),
                hotel=            
            )
def seed_dish_one(pk):
    restaurant=restaurants.objects.get(id=pk)
    for indDish in indian_dishes:
        fake=Faker()
        description = fake.paragraph(nb_sentences=3)  # Generate a paragraph with 3 sentences
        dish=restaurant.dish_set.create(
            dishName=indDish,
            description=description,
            price=random.randint(100,999),
            restaurants=restaurant,
            user=random.choice(user_list),
            hotel=hotel_obj            
        )
def seed_dish_delete():
    restaurant=restaurants.objects.all()
    for rest in restaurant:
        for dish in rest.dish_set.all():
            dish.delete()
def upload_images():
    dishes=dish.objects.all()
    director=rf"C:\Users\Vijay\django_pro\hotels\media\images"
    files=glob.glob(os.path.join(director,"*"))
    a=""
    for obj in dishes:
        for file in files:
            # print(file)
            slite_file=file.split("/")
            for f in slite_file:
                if obj.dishName.lower() in f.lower():
                    # print("done")
                    obj.dishImage=f
                    obj.save() 
def upload_images_one(restid):  
    restaurant=restaurants.objects.get(id=restid)
    dishes=restaurant.dish_set.all()
    director=rf"C:\Users\Vijay\django_pro\hotels\media\images"
    files=glob.glob(os.path.join(director,"*"))
    a=""
    for obj in dishes:
        for file in files:
            # print(file)
            slite_file=file.split("/")
            for f in slite_file:
                if obj.dishName.lower() in f.lower():
                    print("done")
                    obj.dishImage=f
                    obj.save()           
def register_user_to_send_mail(receiver_email,fullname):
    # hotel_obj=hotel.objects.get(id=3)
    hotel_name="vj Hotels"
    subject=f"Welcome to {hotel_name} – Your Account is Ready!"
    email_content = f"""
Subject: Welcome to {hotel_name} – Your Account is Ready!

Dear {fullname},

Thank you for creating an account with {hotel_name}! We're thrilled to have you join our community.

Explore our website to discover a variety of delicious dishes crafted by our expert chefs. Whether you crave savory, sweet, or anything in between, we have something to satisfy every palate.

Visit us at #Vj_hotel.com and start your culinary adventure today!

Bon appétit!

Best regards,
Vijay Gholve
{hotel_name} Team
"""   
    sender=settings.EMAIL_HOST_USER
    try:
        send_mail(subject,email_content,sender,receiver_email)
    except Exception as e:
        # message.error)
        print(e)


def email_for_otp_verification(receiver_email,fullname,otp):
    hotel_obj="vj"
    hotel_name=hotel_obj.name
    subject=f"Welcome to {hotel_name} – Your Account is Ready!"
    email_content = f"""
Subject: Welcome to {hotel_name} – Your Account is Ready!

Dear {fullname},

hii


Best regards,
Vijay Gholve
{hotel_name} Team
"""   
    sender=settings.EMAIL_HOST_USER
    try:
        send_mail(subject,email_content,sender,receiver_email)
    except Exception as e:
        # message.error)
        print(e)
    


def send_mail_to_all_seed():
    hotel_name="vj"
    subject=f"Welcome to {hotel_name} – Your Account is Ready!"
    for i in users:
        email_content = f"""
    Subject: Welcome to {hotel_name} – Your Account is Ready!

    Dear {i.username},

    Thank you for choosing our services. To complete your verification process, please use the One-Time Password (OTP) provided below:



    This OTP is valid for the next 10 minutes. Please enter it on the verification page to proceed.

    If you did not request this verification, please ignore this email or contact our support team immediately.

    Best regards,
    Vijay Gholve
    {hotel_name} Team
    """  
        receipts_list=[i.email]
        sender=settings.EMAIL_HOST_USER
        try:
            send_mail(subject,email_content,sender,receipts_list)
        except Exception as e:
        # message.error)
            print(e)
            


