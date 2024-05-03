from django.forms import ModelForm


from django.contrib.auth.forms import UserCreationForm
from .models import room,User


class RoomForm(ModelForm):
    class Meta:
        model = room
        fields = "__all__"
        exclude = ['host','participants']



class Userform(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','username','email','bio']


class myusercreationform(UserCreationForm):
    class Meta:
        model= User
        fields = ['name','username','email','password1','password2']