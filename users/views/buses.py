from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from ..utility.decorators import IsAdmin
from django.db.models import Avg,Q
from ..utility.errorhandler import CustomError,CustomFunction,Custom_Queryset_Response
from ..utility.custompagination import CustomPageNumberPagination
from users.custom_serializers.buses_serializers import BusListSerializer
from users.models.bus import Bus,Bus_Search_History


class BusesListView(generics.ListAPIView):
    pagination_class = CustomPageNumberPagination
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BusListSerializer
    
    def get_queryset(self):
        search = self.request.GET.get('search')
        queryset = Bus.objects.filter()
        if search != "" and search != None:
            queryset = queryset.filter(Q(bus_details_id__source__istartswith=search) | Q(bus_details_id__destination__istartswith=search) | Q(bus_details_id__date_of_journey__istartswith=search) ).order_by("-id")
            try:
                Bus_Search_History.object.create(user_id=self.request.user.id,search_text=search)
            except:
                pass
        else:
            queryset = queryset.order_by("-id")
        print(queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            data= Custom_Queryset_Response (self,request,self.serializer_class)
            return Response(data)
        except Exception as E:
            data = {"status":500,"message":"Something went wrong!","data":{"trace":str(E)}}
            return Response(data)


class BusDetailView(generics.RetrieveAPIView):
    pagination_class = CustomPageNumberPagination
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = (IsAuthenticated,IsAdmin)
    serializer_class = BusListSerializer
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        queryset = Bus.objects.filter(id=pk)
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            data= Custom_Queryset_Response (self,request,self.serializer_class)
            return Response(data)
        except Exception as E:
            data = {"status":500,"message":"Something went wrong!","data":{"trace":str(E)}}
            return Response(data)