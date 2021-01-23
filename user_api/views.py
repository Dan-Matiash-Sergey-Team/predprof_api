from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as d_login
from django.contrib.auth.models import User
from django.http.response import HttpResponse as hresp
from datetime import datetime
from .models import Record


def regist(request):
    log = request.GET.get('log', None)
    pwd = request.GET.get('pwd', None)
    if log and pwd:
        if User.objects.filter(username=log):
            return hresp(status=400)
        else:
            u = User.objects.create_user(log)
            u.set_password(pwd)
            u.save()
            return hresp(status=200)
    return hresp(status=400)


def login(request):
    log = request.GET.get('log', None)
    pwd = request.GET.get('pwd', None)
    if log and pwd:
        user = authenticate(request, username=log, password=pwd)
        if user is not None:
            d_login(request, user)
            return hresp(status=200)
        else:
            return hresp(status=404)
    return hresp(status=400)


def logut(request):
    if request.user.is_authenticated:
        logout(request)
        return hresp(status=200)
    else:
        return hresp(status=400)


def new_record(request):
    if request.user.is_authenticated:
        v = request.GET.get('value', None)
        if v:
            r = Record.objects.filter(date__date=datetime.now().date(), user=request.user)
            if r.count() == 0:
                r = Record()
                r.value = v
                r.date = datetime.now()
                r.user = request.user
                r.save()
                return hresp(status=200)
            else:
                return hresp(status=400)
        else:
            return hresp(status=400)
    else:
        return hresp(status=403)


def edit_record(request):
    if request.user.is_authenticated:
        v = request.GET.get('value', None)
        if v:
            r = Record.objects.get(date__date=datetime.now().date(), user=request.user)
            if r:
                r.value = v
                r.save()
                return hresp(status=200)
            else:
                return hresp(status=404)
        else:
            return hresp(status=400)
    else:
        return hresp(status=403)


def user_records(request):
    if request.user.is_authenticated:
        return hresp(content=list(Record.objects.filter(user=request.user).values()), status=200)
    else:
        return hresp(status=403)


def get_record(request):
    if request.user.is_authenticated:
        y = request.GET.get('year', None)
        m = request.GET.get('month', None)
        d = request.GET.get('day', None)
        if y and m and d:
            print(list(Record.objects.filter(date__date=datetime(int(y), int(m), int(d)), user=request.user).values()))
            return hresp(content=list(Record.objects.filter(date__date=datetime(int(y), int(m), int(d)), user=request.user).values()),
                         status=200)
        else:
            return hresp(status=400)
    else:
        return hresp(status=403)
