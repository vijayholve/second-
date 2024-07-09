from django.forms import ModelForm
from .models import restaurants


class restaurant_form(ModelForm):
    class Meta:
        model=restaurants
        fields="__all__"
        exclude=["user"]    
     