from django.contrib import admin
from .models import WordOfTheDay, AllFields, Pool
# Register your models here.
admin.site.register(WordOfTheDay)
admin.site.register(AllFields)
admin.site.register(Pool)