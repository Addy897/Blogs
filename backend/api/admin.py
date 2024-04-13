from django.contrib import admin
from .models import EUsers,Blog,Comment
admin.site.register(EUsers)
admin.site.register(Blog)
admin.site.register(Comment)