from django import forms
from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.contrib.auth.forms import UserCreationForm
from .choices import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from allauth.account.signals import user_signed_up
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.forms import IntegerField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null = True, blank = True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,) # validators should be a list
    # associatedWith = models.CharField(max_length=9, choices=school_choices)
    # phone = PhoneNumberField(blank=False, unique=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
         try:
             instance.profile.save()
         except ObjectDoesNotExist:
             Profile.objects.create(user=instance)
         # if created:
         #    Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    birthdate = forms.DateField(required=True)
    phone = forms.CharField(max_length=17)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','birthdate', 'phone', 'password1', 'password2', )

    def __str__(self): # new
        return self.email

    def get_absolute_url(self): # new
        return reverse('sign_up', args=[str(self.id)])

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.birthdate = self.cleaned_data["birthdate"]
        if commit:
            user.save()
        return user

class AdminCreate(object):
     def __init__(self):
         try:
             User.objects.create_superuser (username='user',
                                password='secret',
                                email='pf4tj@virginia.edu')
         except IntegrityError as e:
             logger.warning("DB Error Thrown %s" % e)


class Posting(models.Model):
    book_title = models.CharField(max_length=100,verbose_name='Book Title')
    subject_area = models.CharField(max_length = 4, choices = subject_choices,verbose_name='Subject Area')
    # course_number = models.CharField(max_length = 200)
    class_assoc = models.CharField(max_length = 4,verbose_name = 'Course Number',  help_text = "Please enter in the course number e.g. 3240 for CS3240")
    iSBN = models.CharField(max_length = 200, help_text = "Enter your book's iSBN_13 Please")
    # seller_name = models.CharField(max_length = 200, null = True, blank = True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text = "Please Enter the Price of Your Book in US Dollars")
    contact = models.CharField(max_length = 100)
    rent_buy = models.CharField(max_length = 4, choices = rb_choices,verbose_name='Rent or Buy')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_by', null = True, blank = True)
    image = models.ImageField(upload_to='images/', default='images/default/book_test.png',)

    def __str__(self): # new
        return self.book_title

    def get_absolute_url(self): # new
        return reverse('posting_form', args=[str(self.id)])
