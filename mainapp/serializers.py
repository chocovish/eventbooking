from rest_framework import serializers
from .models import Ticket,Event,User

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = []

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','username','email','age','birthday', 'first_name', 'last_name','image','password']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = []

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

