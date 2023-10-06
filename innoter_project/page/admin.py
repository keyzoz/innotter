from django.contrib import admin

from .models import Followers, Page, Tag

# Register your models here.

admin.site.register(Page)
admin.site.register(Tag)
admin.site.register(Followers)
