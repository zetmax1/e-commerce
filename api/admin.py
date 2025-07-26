from django.contrib import admin
from api.models import Order, OrderItem, CustomUser


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(CustomUser)
