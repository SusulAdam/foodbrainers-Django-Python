from django.urls import path

from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('all/', views.AllRestaurants.as_view(), name='all'),
    path('restaurants/<int:restaurant_id>', views.RestaurantDetails.as_view(), name='details'),

    # jesli nie ma nawiasów w views.add_to_cart to jest to referancja wiec nie ma ()
    path('add_to_cart/<int:course_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('create_order', views.CreateOrder.as_view(), name='create_order'),
]