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



class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        user = self.context["request"].user
        is_pass = user.check_password(data["current_password"])
        if is_pass:
            user.set_password(data["new_password"])
            user.save()
            return user
        raise serializers.ValidationError("Incorrect current password")


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
        extra_kwargs = {'password':{'write_only':True},
                        'image': {'required': False}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Profile(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields=(
            'username',
            'email',
            'first_name',
            'last_name',
            'image',
        )