from celery import shared_task
from .seed import send_mail_to_user_after_order

@shared_task(bind=True)
def send_order_mail_to_user_tasks(seld,pk):
    send_mail_to_user_after_order(pk)
    return "Done"