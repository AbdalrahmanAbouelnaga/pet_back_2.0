from rest_framework.viewsets import ModelViewSet
from .models import Profile
from .serializers import ProfileSerializer,RegisterSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework.response import Response

from rest_framework import generics,permissions
from knox.auth import AuthToken


class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer


    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context.update({"request":self.request})
        return context

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "message":"Password Changed successfully."
        })



class UserInfo(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        return self.request.user

class UpdateInfo(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]
    

    def get_object(self):
        return self.request.user


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer


    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "token":AuthToken.objects.create(user)[1]
        })

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer


    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)









