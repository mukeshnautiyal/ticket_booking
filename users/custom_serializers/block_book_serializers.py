from rest_framework.serializers import (
    Serializer, ModelSerializer, PrimaryKeyRelatedField, CharField
)
from users.models.bus import Bus,Bus_Details
from users.models.block_book import Booking
from users.models.users import User
from rest_framework import serializers


class BookingInfo(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id','bus_number','total_seats','type']
        #depth =1

class BookingBaseSerializer(ModelSerializer):
   
    user = BookingInfo(read_only=True)
    class Meta:
        """ Meta subclass """
        model = Booking
        fields = '__all__'


class BookingListSerializer(BookingBaseSerializer):
    class Meta:
        model = Bus
        fields = ('id','bus_number','total_seats','type')
       
    def to_representation(self, instance):
        try:
            rep = super(BookingListSerializer, self).to_representation(instance)
            #details = User.objects.get(pk=instance.vendor.id)
            return rep    
        except Exception as E:
            print(E)


class BlockSeatSerializer(serializers.Serializer):
    bus_id = serializers.CharField(required=True)
    passengers = serializers.CharField(required=True)
    pickup_point = serializers.CharField(required=True)

class BookSeatSerializer(serializers.Serializer):
    blocking_id = serializers.CharField(required=True)


class UpdateBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['type', 'total_seats']