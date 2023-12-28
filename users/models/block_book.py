from django.db import models
from .users import User
from .bus import Bus

Type_Choice = (
    ("Block Seats","Block Seats"),
    ("Book Seats","Book Seats"),
)

class Booking(models.Model):

    class Meta:
       db_table  = "booking"

    id         =     models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_id",related_query_name="user_user_id")
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True)
    Number_of_passengers = models.IntegerField(null=True, default=None)
    type = models.CharField(max_length=30,choices = Type_Choice, default = 'Block Seats')
    paid        = models.BooleanField(default=True)
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING, related_name="booked_bus_id",related_query_name="booked_bus_bus_id")
    paid_amount = models.IntegerField(default=0)
    pickup_point = models.CharField(max_length=100 ,blank=True)



class Blocking_Bookig_History(models.Model):

    class Meta:
       db_table  = "blocking_bookig_history"

    id         =     models.BigAutoField(primary_key=True)
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="block_book_user",related_query_name="block_book_user_id")
    date      = models.DateTimeField(auto_now_add=True, null=True)
    type = models.CharField(max_length=30,choices = Type_Choice, default = 'Block Seats')
    Number_of_passengers = models.IntegerField(null=True, default=None)
    bus = models.ForeignKey(Bus, on_delete=models.DO_NOTHING, related_name="block_book_bus_id",related_query_name="block_book_bus_bus_id")
    paid_amount = models.IntegerField(default=0)
    pickup_point = models.CharField(max_length=100 ,blank=True)

