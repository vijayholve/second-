from celery import shared_task
from .seed import register_user_to_send_mail,send_mail_to_all_seed
import datetime
@shared_task(bind=True)
def send_mail_task(self,email,fullname):
    register_user_to_send_mail([email],fullname)
    times=datetime.datetime.now()
    current_time = times.strftime("%Y-%m-%d %H:%M:%S")
    return f"procced at {current_time} "

@shared_task(bind=True)
def send_mail_to_all_task(self):
    send_mail_to_all_seed()
    return "done"