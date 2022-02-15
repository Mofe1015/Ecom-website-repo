from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("store/", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update-item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("itemdetails/", views.itemdetails, name="itemdetails")
]
