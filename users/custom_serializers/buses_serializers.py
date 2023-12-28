from rest_framework.serializers import (
    Serializer, ModelSerializer, PrimaryKeyRelatedField, CharField
)
from users.models.bus import Bus,Bus_Details
from users.models.users import User
from rest_framework import serializers


class BusInfo(ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id','bus_number','total_seats','type']
        #depth =1

class BusBaseSerializer(ModelSerializer):
   
    user = BusInfo(read_only=True)
    class Meta:
        """ Meta subclass """
        model = Bus
        fields = '__all__'


class BusListSerializer(BusBaseSerializer):
    class Meta:
        model = Bus
        fields = ('id','bus_number','total_seats','type')
       
    def to_representation(self, instance):
        try:
            rep = super(BusListSerializer, self).to_representation(instance)
            details = User.objects.get(pk=instance.vendor.id)
            rep["vendor"] = {"status":details.status,"number_seats_avialable":details.number_seats_avialable,"source":details.source,"stops":details.stops,"destination":details.destination,"date_of_journey":details.date_of_journey}
            return rep    
        except Exception as E:
            print(E)


class AddBusSerializer(serializers.Serializer):
    bus_number = serializers.CharField(required=True)
    total_seats = serializers.CharField(required=True)
    type = serializers.CharField(required=True)


class UpdateBusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['type', 'total_seats']