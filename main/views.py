from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import NewUser
from .models import Likes, Messages
from django.db.models import Q
from django.db.models import Exists, OuterRef
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
import datetime


@csrf_exempt
@login_required(login_url='user:login')
def main(request):
    user = request.user
    all_users = NewUser.objects.all().exclude(id=user.id)
    form = UserForm()
    # breakpoint()
    if request.method == 'POST':
        form = UserForm(request.POST)
        user = request.user
        user.subscription = form.data['sub']
        user.save()
    return render(request, 'main/main.html', {'all_users': all_users[0],
                                              "user": user,'form': form})


@login_required(login_url='user:login')
def reaction(request, id):
    likes = Likes(who=request.user, whom=NewUser.objects.get(id=id), is_liked=request.GET['a'] == '1')
    likes.save()
    return redirect('main:iter')


@csrf_exempt
def messages(request, id):
    if request.method == "POST":
        message = request.POST['message']
        Messages.objects.create(who=request.user, whom=NewUser.objects.get(id=id), message=message)
    all_messages = Messages.objects.all().filter(Q(who=request.user, whom__id=id)|Q(who__id=id, whom=request.user))
    return render(request, 'main/message.html', {'all_messages': all_messages})


def user_matched(request):
    user = request.user
    matched_users = NewUser.objects.filter(
        Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk'), is_liked=True))).filter(
        Exists(Likes.objects.filter(who__id=OuterRef('pk'), whom=user, is_liked=True))
    ).distinct()
    return render(request, 'main/matched.html', {'matched_users': matched_users})


def iter(request):
    user = request.user
    # breakpoint()
    all_users = NewUser.objects.all().exclude(id=user.id)
    all_users = all_users.filter(~Exists(Likes.objects.filter(who=user, whom__id=OuterRef('pk'))))
    # d1 = Likes.objects.filter(who=user, whom__id=OuterRef('pk'))
    # d2 = datetime.datetime.strptime('30/04/2015', "%d/%m/%Y").date()
    if request.user.subscription == 'Standart':
        limitation = 2
        # if Likes.objects.filter(who=user, created=)
    elif request.user.subscription == 'VIP':
        limitation = 3
    else:
        limitation = len(all_users)
    if len(all_users) == 0:
        return redirect('main:main')
    return render(request, 'main/iter.html',
                  {'all_users': all_users[0], "user": user})


