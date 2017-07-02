from django import forms
from .models import UserName, Trip
from django.core.exceptions import ValidationError
import bcrypt, datetime

def validateName(strInput):
    if not strInput.replace(' ','').isalpha():
        return False
    if len(strInput) < 3:
        return False
    return True

def hasNumbers(strInput):
    return any(char.isdigit() for char in strInput)

def hasUpper(strInput):
    return any(char.isupper() for char in strInput)

class login_form(forms.Form):
    user_name = forms.CharField(label='Username:', max_length=45, min_length=3, required=True)
    password = forms.CharField(label='Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)

    def clean_user_name(self):
        thisUsername = self.cleaned_data['user_name']
        if not UserName.objects.filter(user_name=thisUsername).exists():
            raise ValidationError('You Must Register First!')
        return thisUsername

    def clean_password(self):
        form_data = self.cleaned_data
        password = self.cleaned_data['password']
        user_name = form_data.get('user_name')
        try:
            user = UserName.objects.get(user_name = user_name)
        except:
            raise ValidationError('You Must Register First!')
        hashed_pw = user.password
        if bcrypt.hashpw(password.encode(encoding="utf-8", errors="strict"), hashed_pw.encode(encoding="utf-8", errors="strict")) != hashed_pw:
            raise ValidationError('Incorrect password!')
        return password

class register_form(forms.Form):
    user_name = forms.CharField(label='Username:', max_length=45, min_length=3, required=True)
    name = forms.CharField(label='Name:', max_length=45, min_length=3, required=True)
    password = forms.CharField(label='Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password:', max_length=255, min_length=8, required=True, widget=forms.PasswordInput)

    def clean_user_name(self):
        thisUsername = self.cleaned_data['user_name']
        if UserName.objects.filter(user_name=thisUsername).exists():
            raise ValidationError('Username already exists!')
        if len(thisUsername) < 3:
            raise ValidationError('Username should be at least 3 characters')
        return thisUsername

    def clean_name(self):
        name = self.cleaned_data['name']
        if not validateName(name):
            raise ValidationError('Your name should be greater than 2 characters and less than 45 characters and should not contain numbers or symbols')
        return name

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Passwords must contain as least 8 characters/numbers')
        elif not hasNumbers(password):
            raise ValidationError('Password should contain at least 1 number!')
        elif not hasUpper(password):
            raise ValidationError('Passwords require at least 1 uppercase letter!')
        return password

    def clean_confirm_password(self):
        form_data = self.cleaned_data
        password = form_data.get('password')
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Password and Confirm Password must match')
        return confirm_password

class add_trip_form(forms.Form):
    destination = forms.CharField(label='Destination:', max_length=100, min_length=3, required=True)
    description = forms.CharField(label='Description:', max_length=1000, min_length=3, required=True)
    travelDate_from = forms.DateField(label='Travel Date From:', required=True)
    travelDate_to = forms.DateField(label='Travel Date To:', required=True)

    def clean_destination(self):
        destination = self.cleaned_data['destination']
        if len(destination) < 3:
            raise ValidationError('Destination cannot be empty and must be at least 3 characters')
        return destination

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 3:
            raise ValidationError('Description cannot be empty and must be at least 3 characters')
        elif len(description) > 1000:
            raise ValidationError('Description should be less than 1000 characters')
        return description

    # def clean_travelDate_from(self):
    #     form_data = self.cleaned_data
    #     travelDate_from = self.cleaned_data['travelDate_from']
    #     if travelDate_from < datetime.date.today():
    #         raise ValidationError('Travel From Date cannot be before Today!')
    #     return travelDate_from

    def clean_travelDate_to(self):
        form_data = self.cleaned_data
        travelDate_from = form_data.get('travelDate_from')
        travelDate_to = self.cleaned_data['travelDate_to']
        if travelDate_from > travelDate_to:
            raise ValidationError('Travel To Date cannot be before Travel From Date')
        if travelDate_from < datetime.date.today():
            raise ValidationError('Travel From Date cannot be before Today!')
        return travelDate_to
