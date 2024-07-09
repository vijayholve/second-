from django.contrib.auth.models import User
from base.models import restaurants,dish,orders
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
def send_mail_to_user_after_order(pk):
    order_obj=orders.objects.get(id=pk)
    user = order_obj.user
    Subject="Your Order Confirmation"
    sender_email = settings.EMAIL_HOST_USER
    image_path=order_obj.dish.dishImage
    body = f"""
    Dear {user.username},

    Thank you for your order with {order_obj.restaurants.restaurantName}! We are delighted to inform you that your dish, {order_obj.dish.dishName}, has been successfully placed and is now being prepared with the utmost care and attention.

    Here are the details of your order:
    - Dish Ordered: {order_obj.dish.dishName}
    - Delivery Charges: {order_obj.delivery_charges}
    - Total Charges: {order_obj.total_charges}
    - Delivery Location: {order_obj.location}

    We will notify you once your order is ready and out for delivery. Your estimated delivery time is approximately 30 minutes.

    If you have any questions or need to make changes to your order, please feel free to contact us at {sender_email}.

    Thank you for choosing {order_obj.restaurants.restaurantName}. We hope you enjoy your meal!

    Best regards,

    Vijay Gholve
    Manager
    {order_obj.restaurants.restaurantName}
    """ 
    try:
        # Create the email
        email = send_mail(Subject, body, sender_email, [user.email])
        print("email is sended")
    except Exception as e:
        print(f" Not sended:{e}")

    




 
