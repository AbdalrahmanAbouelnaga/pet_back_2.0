from rest_framework.viewsets import ModelViewSet
from .models import Pet,Kind,Breed
from .serializers import KindSerializer,CreatePetSerializer,BreedSerializer,PetSerializer
from rest_framework.response import Response
from rest_framework import permissions,generics,parsers
from django.http import QueryDict

class KindViewSet(ModelViewSet):
    serializer_class = KindSerializer
    lookup_field = 'name'

    def get_queryset(self):
        if self.action == 'detail':
            return Kind.objects.get(name=self.kwargs["name"])
        return Kind.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    

class BreedViewset(ModelViewSet):
    serializer_class = BreedSerializer
    lookup_field = 'name'
    
    def get_queryset(self):
        return Breed.objects.filter(kind__name = self.kwargs["parent_lookup_kind"])


class PetViewset(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser,parsers.FormParser]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Pet.objects.filter(owner__pk = self.request.user.pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePetSerializer
        if self.request.method == 'GET':
            return PetSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request":self.request})
        return context
    def create(self, request, *args, **kwargs):
        req_dict = request.data.dict()
        images = []
        for image in request.FILES.getlist("images"):
            images.append({"image":image})
        
        data = {
            **req_dict,
            "images":images,
        }
        serializer = CreatePetSerializer(data=data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"New Pet added successfully"},status=201)
        return Response(serializer.errors,status=400)
