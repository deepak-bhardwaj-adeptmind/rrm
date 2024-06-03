from django.db import models


class RoomRate(models.Model):
    room_id = models.IntegerField(unique=True)
    room_name = models.CharField(max_length=100)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.room_name} ({self.room_id}) - {self.default_rate}"


class OverriddenRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    overridden_rate = models.DecimalField(max_digits=10, decimal_places=2)
    stay_date = models.DateField()

    def __str__(self):
        return f"{self.room_rate} ({self.overridden_rate}) - {self.stay_date}"


class Discount(models.Model):
    DISCOUNT_TYPES = [
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage'),
    ]
    discount_id = models.IntegerField(unique=True)
    discount_name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.discount_id} ({self.discount_name}) - {self.discount_type} - {self.discount_value}"


class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room_rate} ({self.discount})"
