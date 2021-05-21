from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreateSection(ModelForm):
	class Meta:
		model = Section
		fields = ['section']

class CreateStudent(ModelForm):
	class Meta:
		model = Student_link
		fields = '__all__'
		exclude=['section']

class AvailabilityForm(forms.ModelForm):


	check_in = forms.DateTimeField(required=True, input_formats = ["%Y-%m-%dT%H:%M", ])
	check_out = forms.DateTimeField(required=True, input_formats = ["%Y-%m-%dT%H:%M", ])

	class Meta:
		model = Booking
		fields = ['check_in','check_out']

class book(ModelForm):
    class Meta:
        model=resource_booking
        fields=['select_resource','quantity']
