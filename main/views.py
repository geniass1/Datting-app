from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import NewUser
from .models import Likes
from django.db.models import Q
from django.db.models import Exists, OuterRef


@login_required(login_url='user:login')
def main(request):
    user = request.user
    all_users = NewUser.objects.all().exclude(id=user.id)
    matched_users = NewUser.objects.filter(Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk')))).filter(
        Exists(Likes.objects.filter(who__id=OuterRef('pk'), whom=user))
    ).distinct()
    return render(request, 'main/main.html', {'all_users': list(all_users), "user": user, "matched_users": matched_users})


@login_required(login_url='user:login')
def like(request, id):
    likes = Likes(who=request.user, whom=NewUser.objects.get(id=id))
    likes.save()
    return redirect('main:main')
