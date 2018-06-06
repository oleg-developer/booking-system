from django.contrib import admin

from apps.hotels.models import Order, DistanceType, StreetType, LocationType, \
    EquipmentSection, Hotel, Address, HotelEquipmentItem, EquipmentItem, \
    Guest, HotelRoom, RoomFoodInfo, FoodType, FoodCost, FoodTime
from apps.hotels.models.room import RoomType


admin.site.register(DistanceType)
admin.site.register(StreetType)
admin.site.register(LocationType)
admin.site.register(EquipmentSection)
admin.site.register(Hotel)
admin.site.register(Address)
admin.site.register(EquipmentItem)
admin.site.register(HotelEquipmentItem)

admin.site.register(Guest)
admin.site.register(HotelRoom)
admin.site.register(Order)
admin.site.register(RoomType)
admin.site.register(RoomFoodInfo)
admin.site.register(FoodType)
admin.site.register(FoodCost)
admin.site.register(FoodTime)
