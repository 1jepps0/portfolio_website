from django.contrib import admin
from app.models import *


# Register your models here.
# admin.site.register(CtfWriteup)

class CtfImageInline(admin.TabularInline):  # Use StackedInline for a vertical layout
    model = CtfImage
    extra = 1  # Number of empty image forms shown by default
    fields = ('image',)

@admin.register(CtfWriteup)
class CtfWriteupAdmin(admin.ModelAdmin):
    inlines = [CtfImageInline]
    list_display = ('name', 'category', 'competition', 'point_count', 'date')  # Adjust fields as needed
