from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Section)
admin.site.register(Student_link)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(resource)
admin.site.register(resource_booking)
