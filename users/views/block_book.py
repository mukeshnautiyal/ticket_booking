from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from ..utility.decorators import IsAdmin
from django.db.models import Avg,Q
from ..utility.errorhandler import CustomError,CustomFunction,Custom_Queryset_Response
from ..utility.custompagination import CustomPageNumberPagination
from users.custom_serializers.block_book_serializers import BlockSeatSerializer,BookSeatSerializer,BookingListSerializer
from users.models.block_book import Booking,Blocking_Bookig_History


class Blocking_Booking(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = (IsAuthenticated,IsAdmin)
    block_class = BlockSeatSerializer
    Book_class = BookSeatSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            type = self.request.GET.get("type")
            data = request.data
            response = {'status':200 , "message":"Bus Successfully Booked","data":None}
            if type == "block":
                serializer = self.block_class(data=data)
                if not  serializer.is_valid():
                    data = {"status":400,"message":"Invalid Data","data":{"message":"Invalid Data",'form_errors':serializer.errors}}
                    return Response(data)
                blocking = Booking.objects.create(bus_id=data["bus_id"],user_id=request.user.id,Number_of_passengers=data["passengers"],type="Block Seats",pickup_point=data["pickup_point"])
                try:
                    Blocking_Bookig_History.objects.create(user_id=self.request.user.id,Number_of_passengers=data["passengers"],bus_id=data["bus_id"],pickup_point=data["pickup_point"])
                except:
                    pass
                response["data"] = {"blocking_id":blocking.id}
                response["message"] = "Seats Successfully Blocked"
            else:
                serializer = self.Book_class(data=data)
                if not  serializer.is_valid():
                    data = {"status":400,"message":"Invalid Data","data":{"message":"Invalid Data",'form_errors':serializer.errors}}
                    return Response(data)
                book_bus = Booking.objects.filter(pk=data["blocking_id"])
                try: 
                    book_bus.update(type="Book Seats")
                    Blocking_Bookig_History.objects.create(user_id=self.request.user.id,Number_of_passengers=book_bus[0].Number_of_passengers,bus_id=book_bus[0].bus.id,pickup_point=book_bus[0].pickup_point,type="Book Seats")
                except:
                    pass
                response["data"] = {"booking":data["blocking_id"]}
            return Response(response)
        except Exception as e:
            response = {'status':500 , "message":"Something went wrong","data":None,"trace":str(e)}
            return Response(response)

class BookingListView(generics.RetrieveAPIView):
    pagination_class = CustomPageNumberPagination
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = (IsAuthenticated,IsAdmin)
    serializer_class = BookingListSerializer
    
    def get_queryset(self):
        queryset = Booking.objects.filter(user_id=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            data= Custom_Queryset_Response (self,request,self.serializer_class)
            return Response(data)
        except Exception as E:
            data = {"status":500,"message":"Something went wrong!","data":{"trace":str(E)}}
            return Response(data)


class BookingDetailView(generics.RetrieveAPIView):
    pagination_class = CustomPageNumberPagination
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = (IsAuthenticated,IsAdmin)
    serializer_class = BookingListSerializer
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        queryset = Booking.objects.filter(is_active=True,id=pk)
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            data= Custom_Queryset_Response (self,request,self.serializer_class)
            return Response(data)
        except Exception as E:
            data = {"status":500,"message":"Something went wrong!","data":{"trace":str(E)}}
            return Response(data)