# myapp/urls.py

from django.urls import path
from .views import *


urlpatterns = [
    path('api/users/', CustomUserListView.as_view(), name='user_list'),
    path('api/users/<int:pk>/', CustomUserDetailView.as_view(), name='user_detail'),

    path('api/create_user/', CreateCustomUserView.as_view(), name='create_user_view'),

    path('api/list_api/', HeadersListCreateView.as_view(), name='headers-list-create'),
    path('api/list_api/<int:pk>/', HeadersDetailView.as_view(), name='headers-detail'),
    
    path('api/list_api/', HeadersListCreateView.as_view(), name='headers-list-create'),
    path('api/list_api/<int:pk>/', HeadersDetailView.as_view(), name='headers-detail'),

    path('api/groups/', GroupListView.as_view(), name='group-list-create'),
    path('api/groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),

    path('api/group_header/', GroupHeaderListCreateView.as_view(), name='group-header-create-update-delete'),
    path('api/group_header/<int:group_id>/', GroupHeaderListView.as_view(), name='group-header-list'),

    path('api/user_groups/', UserGroupListCreateView.as_view(), name='user-group-list-create'),

]

