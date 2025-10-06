from django.contrib import admin

from .models import Book, Lending, Payment

# Register your models here.

admin.site.register(Book)
admin.site.register(Lending)
admin.site.register(Payment)
