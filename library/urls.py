from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('books/<int:book_id>/book/', views.create_booking, name='create_booking'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]
