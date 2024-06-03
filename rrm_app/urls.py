from django.urls import path

from rrm_app.views import (
    RoomRateListView,
    RoomRateCreateView,
    RoomRateUpdateView,
    RoomRateDeleteView,
    OverriddenRoomRateListView,
    OverriddenRoomRateCreateView,
    OverriddenRoomRateDeleteView,
    OverriddenRoomRateUpdateView,
    DiscountListView,
    DiscountCreateView,
    DiscountUpdateView,
    DiscountDeleteView,
    RoomDiscountListView,
    RoomDiscountCreateView,
    RoomDiscountUpdateView,
    RoomDiscountDeleteView,
    get_minimum_room_rate
)

urlpatterns = [
    # UI URLs
    path('', RoomRateListView.as_view(), name='room_rate_list'),
    path('room-rates/', RoomRateListView.as_view(), name='room_rate_list'),
    path('room-rates/add/', RoomRateCreateView.as_view(), name='room_rate_create'),
    path('room-rates/<int:pk>/edit/', RoomRateUpdateView.as_view(), name='room_rate_update'),
    path('room-rates/<int:pk>/delete/', RoomRateDeleteView.as_view(), name='room_rate_delete'),

    path('overridden-rates/', OverriddenRoomRateListView.as_view(), name='overridden_rate_list'),
    path('overridden-rates/add/', OverriddenRoomRateCreateView.as_view(), name='overridden_rate_create'),
    path('overridden-rates/<int:pk>/edit/', OverriddenRoomRateUpdateView.as_view(), name='overridden_rate_update'),
    path('overridden-rates/<int:pk>/delete/', OverriddenRoomRateDeleteView.as_view, name='overridden_rate_delete'),

    path('discounts/', DiscountListView.as_view(), name='discount_list'),
    path('discounts/create/', DiscountCreateView.as_view(), name='discount_create'),
    path('discounts/<int:pk>/update/', DiscountUpdateView.as_view(), name='discount_update'),
    path('discounts/<int:pk>/delete/', DiscountDeleteView.as_view(), name='discount_delete'),

    path('room-discounts/', RoomDiscountListView.as_view(), name='room_discount_list'),
    path('room-discounts/create/', RoomDiscountCreateView.as_view(), name='room_discount_create'),
    path('room-discounts/<int:pk>/update/', RoomDiscountUpdateView.as_view(), name='room_discount_update'),
    path('room-discounts/<int:pk>/delete/', RoomDiscountDeleteView.as_view(), name='room_discount_delete'),

    path('minimum-room-rate/', get_minimum_room_rate, name='minimum_room_rate'),
]
