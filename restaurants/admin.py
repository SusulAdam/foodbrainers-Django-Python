from django.contrib import admin
from .models import Cuisine, Course, Restaurant


class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']



class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'latitude', 'longitude', 'opening_hours','min_order_amount']
    list_filter =  ['name', 'latitude', 'longitude', 'opening_hours','min_order_amount']
    search_fields = ['name', 'description', 'opening_hours','min_order_amount']
    ordering = ['opening_hours']
    autocomplete_fields = ['cuisines']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'is_spicy', 'is_vegan', 'is_glutenfree']
    list_filter = ['name', 'price', 'is_spicy', 'is_vegan', 'is_glutenfree']
    search_fields = ['name', 'description', 'price']
    ordering = ['price']



admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
