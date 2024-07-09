from django.core.mail import send_mail
from django.conf import settings
from .models import Room, Booking

from django.contrib.auth.models import User



def send_mail_to_user_after_booking( pk, id):
    room = Room.objects.get(id=pk)
    booking = Booking.objects.get(id=id)
    user = booking.user
    subject = f"Your Upcoming Stay at {room.roomName}– All You Need to Know! 🌟"
    content = f"""Dear {user},

        We are delighted to confirm your booking and can't wait to welcome you to our beautiful property. Your upcoming stay promises to be a memorable one, and we are here to ensure every detail is perfect.
            
        🛏️ Your Room Details:
        Room Type: {room.roomType}
        Check-in Date: {booking.start_date}
        Check-out Date: {booking.end_date}
        Duration: {booking.duration}
        Total Cost: {booking.total_price}

        📍 Location:
        Our hotel is conveniently located at [Hotel Address]. Whether you're here for business or leisure, you'll find our central location ideal for exploring the vibrant surroundings.

        🕒 Check-in & Check-out:
        Check-in Time: From 3:00 PM
        Check-out Time: By 11:00 AM

        We look forward to providing you with an exceptional stay. Thank you for choosing [Hotel Name]. Safe travels, and see you soon!

        Warm Regards,

        Vijay Gholve
        Manager
        Hotel VJ
        vijaygholve77v@gmail.com
        8080028963
        kharadi
        Pune 14 [411014]
        """
    try:
        sender = settings.EMAIL_HOST_USER
        receiver_mail=booking.user.email
        send_mail(subject, content, sender, [receiver_mail])
        print("Email sent")
    except Exception as e:
        print(e)
        
import gspread # type: ignore
from google.oauth2.service_account import Credentials # type: ignore
import os
from base.models import restaurants,dish
def convert_data_into_sheet_for_dish():
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
        
    ]
    cread=Credentials.from_service_account_file("rooms/credentials1.json",scopes=scopes)
    client=gspread.authorize(cread)
    sheet_id="1QylRM8O_PgQIOXEbMH_2J7BDfmDdghMT3KoFzeS-kF4"
    worksheet=client.open_by_key(sheet_id)
    value_list=worksheet.sheet1.row_values(1)
    sheet=worksheet.worksheet("dishes")
    value=sheet.update_acell("A1","hello world")
    dish_obj=dish.objects.all().values_list(
    "dishName"
    ,"description"
    ,"price"
    ,"restaurants"
    ,"user"
    ,"dishImage")
    rest_list=[list(row) for row in dish_obj]

    header=["dishName","description","price","restaurants","user","dishImage"]
    rest_list.insert(0,header)

    sheet.clear()
    sheet.append_rows(rest_list)
# def images_show():
#     for row in data_list[1:]:
#         row[2] = f'=IMAGE("{row[2]}")'
def convert_data_into_sheet_for_user():
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
        
    ]
    cread=Credentials.from_service_account_file("",scopes=scopes)
    client=gspread.authorize(cread)
    sheet_id="1QylRM8O_PgQIOXEbMH_2J7BDfmDdghMT3KoFzeS-kF4"
    worksheet=client.open_by_key(sheet_id)
    value_list=worksheet.sheet1.row_values(1)
    sheet=worksheet.worksheet("users")
    
    User_obj=User.objects.all().values_list("id","username",'email')
    user_list=[list(row) for row in User_obj]

    header=["id","username","email"]
    user_list.insert(0,header)
    sheet.clear()
    sheet.append_rows(user_list)

