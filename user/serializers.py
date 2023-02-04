from rest_framework import serializers
from .models import Profile
from django.urls import reverse
from django.contrib.auth import authenticate



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'image',
            'password'
        )
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Profile(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self,obj):
        return reverse('user-detail',kwargs={'username':obj.username})
    class Meta:
        model=Profile
        fields=(
            'url',
            'username',
            'first_name',
            'last_name',
            'image',
        )