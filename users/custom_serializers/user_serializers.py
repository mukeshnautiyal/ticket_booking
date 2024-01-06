from rest_framework.serializers import (
    Serializer, ModelSerializer, PrimaryKeyRelatedField, CharField
)
from users.models.users import User
from rest_framework import serializers

class UserInfo(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','phone','email','is_active',"address"]
        #depth =1

class UserBaseSerializer(ModelSerializer):
   
    user = UserInfo(read_only=True)
    class Meta:
        """ Meta subclass """
        model = User
        fields = '__all__'


class UserListSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','phone','email','is_active',"address","vendor_code")
       
    def to_representation(self, instance):
        try:
            rep = super(UserListSerializer, self).to_representation(instance)            
            return rep    
        except Exception as E:
            print(E)


class UserAddSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=False,allow_blank=True)


class updateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','address','phone']