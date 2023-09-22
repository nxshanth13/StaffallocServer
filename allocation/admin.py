from django.contrib import admin
from .models import *
class UsersAdmin(admin.ModelAdmin):
    list_display=('name','password','department','email')

class StaffAdmin(admin.ModelAdmin):
    list_display=('name','designation','department','gender','subcode')

class RoomsAdmin(admin.ModelAdmin):
    list_display=['roomno']
admin.site.register(Users,UsersAdmin)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Rooms,RoomsAdmin)
# Register your models here.
