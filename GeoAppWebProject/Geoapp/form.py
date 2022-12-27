from django import forms
from .models import Boundary
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    First_Name = forms.CharField(max_length=100)
    Middle_Name = forms.CharField(max_length=100)
    Surname = forms.CharField(max_length=100)
    Email= forms.EmailField()
    class Meta:
        model = User
        fields = ['First_Name', 'Middle_Name', 'Surname','Email','username','password1','password2']

        
class DetailsForm(forms.ModelForm):
    Parcel_ID_1 = forms.IntegerField(required=False)
    Parcel_ID_2 = forms.IntegerField(required=False)
    Parcel_ID_3 = forms.IntegerField(required=False)
    class Meta:
        model = Boundary
        fields= ['Parcel_ID_1','Parcel_ID_2','Parcel_ID_3']