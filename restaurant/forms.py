from django.forms import ModelForm,FileInput,ClearableFileInput,ImageField
from base.models import restaurants,Images


class restaurant_form(ModelForm):
    class Meta:
        model=restaurants
        fields="__all__"
        exclude=["user"]  
        
