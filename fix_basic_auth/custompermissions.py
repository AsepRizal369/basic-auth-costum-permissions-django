from django.db import connection
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class CustomPermission(permissions.BasePermission):
    permission_name = ""
    type_permission = ""

    def __init__(self, permission_name, type_permission):
        super().__init__()
        self.permission_name = permission_name
        self.type_permission = type_permission

    def __call__(self):
        return self
        
    def has_permission(self, request, view):
            
        if request.user.is_authenticated:
            return self.has_object_permission(request)
        else :
            return False

    def has_object_permission(self, request):
        
        with connection.cursor() as cursor:    
            sql = "SELECT fn_permission(%s, '%s', '%s')"%(request.user.id, self.permission_name, self.type_permission)
            # print(sql)

            cursor.execute(sql)
            row = cursor.fetchone()
            if row[0] == 1:
                return True
            else :
                raise PermissionDenied("You do not have permission to perform this action.")