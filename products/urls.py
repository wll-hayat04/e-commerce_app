from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/increase/<int:id>/", views.increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:id>/", views.decrease_quantity, name="decrease_quantity"),
    path("cart/coupon/apply/", views.apply_coupon, name="apply_coupon"),
    path("cart/coupon/remove/", views.remove_coupon, name="remove_coupon"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/toggle/<int:id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:id>/", views.order_detail, name="order_detail"),
    path("orders/<int:id>/confirm/", views.order_confirm, name="order_confirm"),
    path("orders/<int:id>/cancel/", views.cancel_order, name="cancel_order"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter"),
]