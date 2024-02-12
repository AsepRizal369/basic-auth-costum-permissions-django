from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    expired = models.DateTimeField(null=True, blank=True)

class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    insert_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    insert_dtm = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    update_dtm = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.name

class Headers(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    api_name = models.CharField(max_length=255, unique=True)
    insert_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    insert_dtm = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    update_dtm = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return f"{self.api_name} - {self.app_name} - {self.project_name}"


class UserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    insert_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    insert_dtm = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    update_dtm = models.DateTimeField(auto_now=True,null=True, blank=True)

class GroupHeader(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    header = models.ForeignKey(Headers, on_delete=models.CASCADE)
    insert_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    insert_dtm = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    update_dtm = models.DateTimeField(auto_now=True,null=True, blank=True)

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    name_api = models.CharField(max_length=255)
    request = models.TextField()
    response = models.TextField(null=True, blank=True)
    insert_dtm = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name_api} - ID: {self.id}"

