from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from apps.auth_core.viewsets import AuthViewSet
from apps.common.viewsets import CountryViewSet
from apps.hotels.viewsets import HotelViewSet, HotelEquipmentViewSet, \
    GuestsViewSet, BookingViewset
from apps.users.viewsets import StaffViewSet

router = DefaultRouter()

admin.autodiscover()

router.register('auth', AuthViewSet, base_name='auth')
router.register('countries', CountryViewSet, base_name='countries')
router.register('staff', StaffViewSet, base_name='staff')
router.register('hotel/equipment', HotelEquipmentViewSet,
                base_name='hotel_equipment')
router.register('hotel', HotelViewSet, base_name='hotel')
router.register('guests', GuestsViewSet, base_name='guests')
router.register('booking', BookingViewset, base_name='booking')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.get_urls())),
    # additional views used for displaying templates or redirects
    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]
