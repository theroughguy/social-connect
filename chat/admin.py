from django.contrib import admin
from .models import room,Messages,Topic,User
# Register your models here.
admin.site.register(room)

admin.site.register(Messages)
admin.site.register(Topic)
admin.site.register(User)



