from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DonorSignup, Profile, Messages
# Register your models here.

class DonorAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'age', 'gender', 'phone', 'blood_group')
    search_fields = ('email', 'name', 'age', 'phone', 'blood_group')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class MessageAdmin(admin.ModelAdmin):
    list_display = ('email_from', 'message', 'email_to')
    search_fields = ('email_from', 'message', 'email_to')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(DonorSignup, DonorAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Messages, MessageAdmin)