from django.db import models
from .users import User

Status_Choice = (
    ("Waiting","Waiting"),
    ("Start","Start"),
    ("On The Way","On The Way"),
    ("Completed","Completed"),
    ("Canceled","Canceled"),
)

Type_Choice = (
    ("AC","AC"),
    ("Non AC","Non AC"),
)


class Bus(models.Model):

    class Meta:
       db_table  = "bus"

    id         =     models.BigAutoField(primary_key=True)
    bus_number        = models.CharField(max_length=20, unique=True,blank=True)
    total_seats = models.IntegerField(null=True, default=None)
    type = models.CharField(max_length=30,choices = Type_Choice, default = 'Non AC')
    is_active        = models.BooleanField(default=False)
    is_deleted        = models.BooleanField(default=False)

    def __str__(self):
        return self.bus_number


class Bus_Details(models.Model):

    class Meta:
       db_table  = "bus_details"

    id         =     models.BigAutoField(primary_key=True)
    bus        = models.ForeignKey(Bus, on_delete=models.DO_NOTHING, related_name="bus_details_id",related_query_name="bus_id")
    status = models.CharField(max_length=30,choices = Status_Choice, default = 'Waiting')
    number_seats_avialable = models.IntegerField(null=True, default=None)
    source = models.CharField(max_length=100 ,blank=True)
    stops = models.CharField(max_length=255 ,blank=True,null=True)
    destination = models.CharField(max_length=100, blank=True)
    date_of_journey = models.DateTimeField(auto_now=True,blank=True, null=True)
    departure           = models.DateTimeField(auto_now=True,blank=True, null=True)
    arrival           = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return self.status

class Bus_Stops(models.Model):
    class Meta:
       db_table  = "bus_stops"

    id         =     models.BigAutoField(primary_key=True)
    bus        = models.ForeignKey(Bus_Details, on_delete=models.DO_NOTHING, related_name="bus_stop_id",related_query_name="stop_id")
    name = models.CharField(max_length=30,choices = Status_Choice, default = 'Waiting')

class Bus_Search_History(models.Model):

    class Meta:
       db_table  = "bus_search_history"

    id         =     models.BigAutoField(primary_key=True)
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="bus_search_user",related_query_name="bus_search_user_id")
    searched_on      = models.DateTimeField(auto_now_add=True)
    search_text = models.CharField(max_length=255 ,blank=True,null=True)

