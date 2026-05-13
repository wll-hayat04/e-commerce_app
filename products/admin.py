from django.contrib import admin
from .models import (Category, Product, Review,
                     Wishlist, Order, OrderItem, Coupon, Newsletter)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'stock',
                    'category', 'is_featured', 'views_count', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_featured', 'stock', 'price')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'discount_amount',
                    'status', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'total', 'discount_amount', 'created_at')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_active', 'valid_until')
    list_editable = ('is_active',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')