# tasks.py
import logging
from celery import shared_task
from .seed import send_mail_to_user_after_booking
from .models import Room, Booking

# Configure logging
logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_mail_booking_task(self, room_id, booking_id):
    logger.info(f"send_mail_booking_task called with room_id={room_id} and booking_id={booking_id}")
    try:
        send_mail_to_user_after_booking(room_id, booking_id)
        logger.info(f"Email sent for booking_id={booking_id}")
        return "DONE"   
    except Room.DoesNotExist:
        logger.error(f"Room with id={room_id} not found")
        return "Failed: Room not found."
    except Booking.DoesNotExist:
        logger.error(f"Booking with id={booking_id} not found")
        return "Failed: Booking not found."
    except Exception as e:
        logger.error(f"Error in send_mail_booking_task: {e}")
        return f"Failed: {e}"
