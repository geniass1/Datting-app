from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import NewUser
from .models import Likes, Messages
from django.db.models import Q
from django.db.models import Exists, OuterRef
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import jwt

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserMatchedSerializer, MessageSerializer, ReactionSerializer


class Reaction(APIView):
    def post(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], "secret", algorithms=["HS256"])
        user = NewUser.objects.get(username=username['username'])
        today_limit = len(Likes.objects.all().filter(who=user, created=datetime.now()))
        data = dict(request.data.items())
        data['who'] = user.id
        data['whom'] = id
        if user.subscription == 'Standart':
            limitation = 2
        elif user.subscription == 'VIP':
            limitation = 3
        else:
            limitation = len(NewUser.objects.all().exclude(id=user.id))
        if today_limit == limitation:
            return Response({"ERROR"})
        serializer = ReactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class Message(APIView):
    def get(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], "secret", algorithms=["HS256"])
        user = NewUser.objects.get(username=username['username'])
        all_messages = Messages.objects.all().filter(
            Q(who=user, whom__id=id) | Q(who__id=id, whom=user))
        all_messages = [MessageSerializer(instance=message).data for message in all_messages]
        return Response({'all_messages': all_messages})

    def post(self, request, id):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], "secret", algorithms=["HS256"])
        data = dict(request.data.items())
        data['who'] = NewUser.objects.get(username=username['username']).id
        data['whom'] = id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UserMatched(APIView):
    def get(self, request, *args, **kwargs):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], "secret", algorithms=["HS256"])
        user = NewUser.objects.get(username=username['username'])
        qs = NewUser.objects.filter(
            Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk'), is_liked=True))).filter(
            Exists(Likes.objects.filter(who__id=OuterRef('pk'), whom=user, is_liked=True))
        ).distinct()
        serializers = UserMatchedSerializer(qs, many=True)
        return Response(serializers.data)


class Iter(APIView):
    def get(self, request):
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], "secret", algorithms=["HS256"])
        user = NewUser.objects.get(username=username['username'])
        today_limit = len(Likes.objects.all().filter(who=user,
                                                     created=datetime.now()))
        all_users = NewUser.objects.all().exclude(id=user.id)
        all_users = all_users.filter(~Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk'))))
        if user.subscription == 'Standart':
            limitation = 2
        elif user.subscription == 'VIP':
            limitation = 3
        else:
            limitation = len(NewUser.objects.all().exclude(id=user.id))
        if today_limit == limitation:
            return Response({'Limitation is full'})
        return Response({'username': str(all_users[0]), 'id': all_users[0].id})
