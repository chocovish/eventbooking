from django.shortcuts import render, HttpResponse
from .models import User
from django.contrib.auth import logout
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import date

from .serializers import TicketSerializer,UserSerializer,EventSerializer,ChangePasswordSerializer
from .models import Ticket, Event


def home(request):
    return HttpResponse("HEllo World !!")

class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def create(self,request):
        sr = UserSerializer(data=request.data)
        if sr.is_valid():
            u = User.objects.create_user(username=sr.data['username'],email=sr.data['email'],password=sr.data['password'])
            return Response(UserSerializer(u).data)
        return Response(sr.errors)

class ChangePasswordView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try: object = User.objects.get(pk=pk)
        except: return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            object.set_password(serializer.data.get("new_password"))
            object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def get(self, request, format=None):
        try: request.user.auth_token.delete()
        except: pass
        if self.request.user.is_authenticated:
            logout(request)
        return Response(status=status.HTTP_200_OK)

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventFilter(APIView):
    def get(self, request, format=None):
        filter = request.GET.get('filterby',False)
        value = request.GET.get("value", False)

        if not filter or not value: return Response(status=status.HTTP_400_BAD_REQUEST)

        if filter=="location": qs = Event.objects.filter(location__iexact=value)
        elif filter=="trending": qs = Event.objects.filter(trending=bool(value))
        elif filter=="upcoming":
            d = date.today()
            qs = Event.objects.filter(date__gt=d)
        elif filter=="date":
            d = date(year=int(value[:4]),month=int(value[4:6]),day=int(value[6:8]))
            qs = Event.objects.filter(date=d)
        e = EventSerializer(qs,many=True)
        return Response(e.data)


class EventsBookedByUser(APIView):
    def get(self, request, pk, format=None):
        try: u = User.objects.get(pk=pk)
        except: return Response(status=status.HTTP_404_NOT_FOUND)
        
        qs = u.ticket_set.all().values_list("event",flat=True)
        qs = Event.objects.filter(pk__in=qs)
        events = EventSerializer(qs, many=True)
        return Response(events.data)

