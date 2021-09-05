from django.contrib import admin
from my_user.models import User,History
# Register your models here.
admin.site.register([User,History])