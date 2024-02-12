# myapp/serializers.py

from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    expired = serializers.DateTimeField(required=True)  # Set required=True

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'expired')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        expired = validated_data.pop('expired')
        user = User.objects.create_user(**validated_data, expired=expired)
        return user
    
    def is_accessible_by_user(self, user):
        # Implement your custom logic here to check if the user has permission
        # Example: Check if the user is in a specific group or has a specific attribute
        return user.groups.filter(name='test').exists()

    
class HeadersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headers
        fields = ('id', 'project_name', 'app_name', 'api_name', 'insert_dtm')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description','insert_dtm')

class GroupHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupHeader
        fields = ['id', 'group', 'header','insert_dtm']

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'



