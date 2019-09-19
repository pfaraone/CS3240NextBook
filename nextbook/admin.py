from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# superuser: admin, 1234

# Register your models here.
from .models import Posting, Profile
admin.site.register(Posting)
admin.site.register(Profile)

class ArticleAdmin(admin.ModelAdmin):
    fields= ['book_title', 'iSBN', 'class_assoc', 'seller_name', 'price', 'contact', 'rent_buy', 'user']
    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance,'posted_by'):
            instance.created_by = request.user
        instance.save()
        form.save_m2m()
        return instance
