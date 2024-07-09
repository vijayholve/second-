from django.db import models
from base.models import restaurants,Room
from django.contrib.auth.models import User
class message(models.Model):
    text = models.TextField()
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender_message")
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver_message")
    restaurant=models.ForeignKey(restaurants,on_delete=models.CASCADE,null=True,blank=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE,related_name="room_message",null=True,blank=True)
    added=models.DateTimeField(auto_now_add=True)
    seen=models.BooleanField(default=False)
    def __str__(self):
        obj=self.restaurant or self.room or  ""
        return f"message is {self.text  } sended by {self.sender} to {self.receiver} " 
    class Meta:
        ordering=["id"]