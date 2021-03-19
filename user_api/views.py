from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as d_login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse as hresp
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from datetime import datetime
from .models import Record
from .serializers import RecordSerializer, UserSerializer
import json


@csrf_exempt
def register(request):
    log = json.loads(request.body)['login'] or None
    pwd = json.loads(request.body)['password'] or None
    if log and pwd:
        if User.objects.filter(username=log):
            return hresp(status=409)
        else:
            u = User.objects.create_user(log)
            try:
                validate_password(pwd, u)
            except Exception as e:
                u.delete()
                return hresp(status=411, content=json.dumps(str(e)))
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


def logout(request):
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
        d = request.GET.get('date', None)
        if v:
            r = Record.objects.get(date__date=(datetime.strptime(d, "%Y-%m-%d")).date(), user=request.user)
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
            return hresp(content=list(
                Record.objects.filter(date__date=datetime(int(y), int(m), int(d)), user=request.user).values()),
                status=200)
        else:
            return hresp(status=400)
    else:
        return hresp(status=403)


class RecordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        records = Record.objects.filter(user=request.user)
        serializer = RecordSerializer(records, many=True)
        return Response({"records": serializer.data}, status=200)

    def post(self, request):
        record = request.data.get('record')
        record['user'] = {'id': request.user.id, 'username': request.user.username}
        record['date'] = datetime.now()
        serializer = RecordSerializer(data=record)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(status=400)

    def put(self, request):
        data = request.data.get('record')
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d')
        record = get_object_or_404(Record.objects.filter(user=request.user), date__date=data['date'].date())
        serializer = RecordSerializer(instance=record, data=data, partial=True)
        print(serializer.is_valid(raise_exception=True))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=200)
        return Response(status=400)

# git add --all
# git commit -m a
# git push -u origin master
#