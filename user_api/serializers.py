from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Record
from django.contrib.auth.validators import UnicodeUsernameValidator
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


def check_weight(val):
    return 0 < val < 300


class RecordSerializer(serializers.Serializer):
    value = serializers.FloatField(allow_null=False, validators=[check_weight])

    date = serializers.DateTimeField(allow_null=False)

    user = UserSerializer()

    def validate_user(self, value):
        if Record.objects.filter(date__date=datetime.now().date(), user__username=value['username']).count() == 0:
            return User.objects.get(username=value['username'])
        raise serializers.ValidationError("Today already was a record")

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        instance.value = validated_data.get('value', instance.value)
        instance.data = validated_data.get('date', instance.date)
        instance.user = instance.user
        instance.save()
        return instance
