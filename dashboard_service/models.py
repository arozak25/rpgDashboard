from django.db import models


class BookingEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    hotel_id = models.IntegerField()
    timestamp = models.DateTimeField()
    rpg_status = models.IntegerField()
    room_id = models.IntegerField()
    night_of_stay = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return self.id

