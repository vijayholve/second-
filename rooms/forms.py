from django.forms import ModelForm
from .models import Room,Booking

class room_form(ModelForm):
    
    class Meta:
        model=Room
        fields="__all__"
        exclude=["user","hotels"]

    # def __init__(self, *args, **kwargs):
    #     super(room_form, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['placeholder'] = field.label
    #         field.widget.attrs['class'] = 'login__input'







