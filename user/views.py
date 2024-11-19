from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, C, GenericViewSet

from user.models import Customer
from user.serializers import UserSerializer


# Create your views here.


class UserRegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = UserSerializer
