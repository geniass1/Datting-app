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


@csrf_exempt
@login_required(login_url='user:login')
def main(request):
    user = request.user
    all_users = NewUser.objects.all().exclude(id=user.id)
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        user = request.user
        user.subscription = form.data['sub']
        user.save()
    return render(request, 'main/main.html', {'all_users': all_users[0],
                                              "user": user,'form': form})


@login_required(login_url='user:login')
def reaction(request, id):
    user = request.user
    today_limit = len(Likes.objects.all().filter(who=request.user, created=datetime.now()))
    all_users = NewUser.objects.all().exclude(id=user.id)
    if request.user.subscription == 'Standart':
        limitation = 2
    elif request.user.subscription == 'VIP':
        limitation = 3
    else:
        limitation = len(all_users)
    if today_limit == limitation:
        return redirect('main:main')
    likes = Likes(who=request.user, whom=NewUser.objects.get(id=id), is_liked=request.GET['a'] == '1')
    likes.save()
    return redirect('main:iter')


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


@csrf_exempt
def messages(request, id):
    if request.method == "POST":
        message = request.POST['message']
        Messages.objects.create(who=request.user, whom=NewUser.objects.get(id=id), message=message)
    all_messages = Messages.objects.all().filter(Q(who=request.user, whom__id=id)|Q(who__id=id, whom=request.user))
    return render(request, 'main/message.html', {'all_messages': all_messages})


class Message(APIView):
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


def user_matched(request):
    user = request.user
    matched_users = NewUser.objects.filter(
        Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk'), is_liked=True))).filter(
        Exists(Likes.objects.filter(who__id=OuterRef('pk'), whom=user, is_liked=True))
    ).distinct()
    return render(request, 'main/matched.html', {'matched_users': matched_users})


class UserMatched(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        qs = NewUser.objects.filter(
            Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk'), is_liked=True))).filter(
            Exists(Likes.objects.filter(who__id=OuterRef('pk'), whom=user, is_liked=True))
        ).distinct()
        serializers = UserMatchedSerializer(qs, many=True)
        return Response(serializers.data)


def iter(request):
    user = request.user
    today_limit = len(Likes.objects.all().filter(who=request.user, created=datetime.now()))
    all_users = NewUser.objects.all().exclude(id=user.id)
    all_users = all_users.filter(~Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk'))))
    if request.user.subscription == 'Standart':
        limitation = 2
    elif request.user.subscription == 'VIP':
        limitation = 3
    else:
        limitation = len(NewUser.objects.all().exclude(id=user.id))
    if today_limit == limitation:
        return redirect('main:main')
    return render(request, 'main/iter.html',
                  {'all_users': all_users[0], "user": user})


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
