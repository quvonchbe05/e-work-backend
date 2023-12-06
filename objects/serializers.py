from rest_framework import serializers
from .models import Object
from accounts.models import CustomUser


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class UserForObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'username', 'phone')


class ObjectListSerializer(serializers.ModelSerializer):
    worker = UserForObjectSerializer()

    class Meta:
        model = Object
        fields = ('id', 'name', 'address', 'worker')
