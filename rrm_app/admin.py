from django.contrib import admin
from .models import RoomRate, OverriddenRoomRate, Discount, DiscountRoomRate

admin.site.register(RoomRate)
admin.site.register(OverriddenRoomRate)
admin.site.register(Discount)
admin.site.register(DiscountRoomRate)
