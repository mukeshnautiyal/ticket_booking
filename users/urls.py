from django.urls import path
#importing tokens 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views.user import *
from users.views.user_signin import LoginView
from users.views.buses import *
from users.views.block_book import *


urlpatterns = [
    #User URL's
    path('signin', LoginView.as_view(), name='signin'),
    path('user/create/', CreateUser.as_view(), name='create_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/list', UserListView.as_view(), name='user_list'),
    path('user/details/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    #Booking URL's
    path('buses/list', BusesListView.as_view(), name='buses_list'),
    path('buses/details/<int:pk>/', BusDetailView.as_view(), name='buses_detail'),
    
    #Booking URL's
    path('booking/list/', BookingDetailView.as_view(), name='booking_detail'),
    path('booking/blocking_booking/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
]