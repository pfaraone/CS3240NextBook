# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
from django.contrib.admin import widgets
from django.utils.timezone import now
from django.core.validators import RegexValidator
from .models import *
from .choices import *
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.utils import timezone
from django.forms import IntegerField

class SignUpForm(forms.Form):
    # UserCreateForm
    #forms.ModelForm
    date_range = 80
    this_year = now().year
    first_name = forms.CharField(max_length=30, required=True, help_text='required')
    last_name = forms.CharField(max_length=30, required=True, help_text='required')
    email = forms.EmailField(max_length=254, required=True, help_text='required')
    birthdate = forms.DateField(
         initial=datetime.date.today(),
         widget=SelectDateWidget(years = range(this_year - date_range, this_year - 14),
         empty_label=("Choose Year", "Choose Month", "Choose Day"),
         ),
     )
    # phone = PhoneNumberField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(max_length=17, required=False,help_text='Enter in your mobile number')
    # phone = PhoneNumberField(blank=True, help_text='Contact phone number')
    # associatedWith = forms.Charfield(max_length=9, choices=school_choices)
    # phone = PhoneNumberField(blank=True, unique=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','birthdate', 'phone_number','phone', 'password1', 'password2', )
    # profile.user.last_login == profile.user.date_joined
    def signup(self, request, user):
        # user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.profile.birthdate = self.cleaned_data['birthdate']
        user.profile.phone_number = self.cleaned_data['phone_number']
        # user.profile.associatedWith = self.cleaned_date['associatedWith']
        user.save()

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=False)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

class ProfileEditForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=17, required=False,help_text='Enter Phone Number in format: +1XXXXXXXXXX')
    class Meta:
        model = Profile
        fields = ('phone_number',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)

class PostingForm(forms.ModelForm):
    required_css_class = 'required'
    book_title = forms.CharField(label='Your book title',max_length=100, required=True)
    subject_area = forms.CharField(max_length = 4,required = True)
    class_assoc = forms.CharField(max_length = 4,required = True, help_text = "Please enter in the course number e.g. 3240 for CS3240")
    iSBN = forms.CharField(max_length = 200, help_text = "Enter your book's iSBN_13 please", required = True)
    price = forms.DecimalField(required = True)
    contact = forms.CharField(max_length = 100 )
    rent_buy = forms.CharField(max_length = 4, )
    image = forms.ImageField()
    class Meta:
        model = Posting
        fields = ('book_title', 'subject_area', 'class_assoc', 'iSBN', 'price', 'rent_buy', 'image')
