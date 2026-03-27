from django.contrib import admin

# Register your models here.


from .models import UserProfile,BakerProfile

admin.site.register(UserProfile)
admin.site.register(BakerProfile)