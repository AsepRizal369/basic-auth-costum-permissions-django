# myapp/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .models import Headers
from rest_framework import status
from fix_basic_auth.custompermissions import *
from django.utils import timezone



class CustomUserListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        CustomPermission('api_name', 'admin').has_permission(request, self)
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        self.save_custom_log(request,serializer)
        return Response(serializer.data)
    
    def save_custom_log(self, request,serializer):
        results = [
            dict(row) for row in serializer.data
        ]

        log_entry = Log(
            name_api=request.path,
            request=request.body.decode('utf-8'),
            response=results,
            insert_dtm=timezone.now(),
            user_id=self.request.user.id if self.request.user.is_authenticated else None
        )
        log_entry.save()


class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateCustomUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class HeadersListCreateView(generics.ListCreateAPIView):
    queryset = Headers.objects.all()
    serializer_class = HeadersSerializer
    permission_classes = [permissions.IsAuthenticated]

class HeadersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Headers.objects.all()
    serializer_class = HeadersSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupListView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupHeaderListCreateView(APIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data

        # Cari GroupHeader berdasarkan group_id di request
        group_id = request_data[0]['group']
        existing_group_headers = GroupHeader.objects.filter(group_id=group_id)

        # Delete semua GroupHeader yang terkait dengan group_id
        existing_group_headers.delete()

        # Buat serializer dari data request dan simpan ke database
        serializer = GroupHeaderSerializer(data=request_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupHeaderListView(APIView):
    def get(self, request, group_id, *args, **kwargs):
        group_headers = GroupHeader.objects.filter(group_id=group_id)
        serializer = GroupHeaderSerializer(group_headers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserGroupListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        user_groups = UserGroup.objects.all()
        serializer = UserGroupSerializer(user_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_groups_data = request.data

        # Hapus semua UserGroup untuk setiap user dalam request
        user_ids = set(item['user'] for item in user_groups_data)
        UserGroup.objects.filter(user__in=user_ids).delete()

        # Simpan UserGroup baru
        serializer = UserGroupSerializer(data=user_groups_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




