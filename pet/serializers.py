from rest_framework import serializers
from .models import Pet,Kind,Breed,PetImages
from django.urls import reverse
from datetime import date
import time
from user.models import Profile


class BreedSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    def get_url(self,obj):
        return reverse('breed-detail',kwargs={'parent_lookup_kind':obj.kind.name,'name':obj.name})

    class Meta:
        model = Breed
        fields = (
            'url',
            'name',
        )


class KindSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    def get_url(self,obj):
        return reverse('kind-detail',kwargs={'name':obj.name})
    breeds = BreedSerializer(many=True)

    class Meta:
        model = Kind
        fields = (
            'url',
            'name',
            'breeds',
        )




class CreatePetImageSerializer(serializers.Serializer):
    image = serializers.ImageField()




class CreatePetSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    breed = serializers.CharField()
    kind = serializers.CharField()
    birth_date = serializers.DateField()
    images = CreatePetImageSerializer(many=True)

    class Meta:
        model = Pet
        fields = (
            'id',
            'name',
            'breed',
            'kind',
            'birth_date',
            'images'
        )
    
    def create(self, validated_data):
        images = validated_data.pop("images")
        owner = Profile.objects.get(pk=self.context["request"].user.pk)
        print(owner)
        if not len(images):
            raise serializers.ValidationError('Pet images are required')
        if not validated_data["name"]:
            raise serializers.ValidationError("Pet name is required")
        if not validated_data["kind"]:
            raise serializers.ValidationError("Pet kind is required")
        if not validated_data["breed"]:
            raise serializers.ValidationError("Pet breed is required")
        if not validated_data["birth_date"]:
            raise serializers.ValidationError("Pet birth date is required")
        breed_name = validated_data.pop("breed")
        kind_name = validated_data.pop("kind")
        try:
            breed = Breed.objects.get(name=breed_name)
        except Breed.DoesNotExist:
            try:
                kind = Kind.objects.get(name = kind_name)
            except:
                kind = Kind(name=kind_name)
                kind.save()
            breed = Breed(name=breed_name,kind=kind)
            breed.save()
        print(breed.name)
        pet = Pet.objects.create(owner =owner,breed=breed,**validated_data)
        for image in images:
            img = PetImages(pet = pet,image=image.get("image"))
            img.save()
        pet.save()
        return pet

class PetImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    thumbnail = serializers.ImageField()
    class Meta:
        model = PetImages
        fields = (
            'image',
            'thumbnail'
        )


class PetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True)
    age = serializers.SerializerMethodField()
    # url = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField()


    def get_breed(self,obj):
        return obj.breed.name

    # def get_url(self,obj):
    #     return reverse('user-pets-detail',kwargs={
    #         'parent_lookup_owner_slug':obj.owner.slug,
    #         'slug':obj.slug
    #     })

    def get_age(self,obj):
        birthdate = obj.birth_date
        today = date.today()
        if today.year-birthdate.year <2:
            td =  today-birthdate
            format='%m-%d'
            time_obj = time.gmtime(td.total_seconds())
            return f'{time_obj.tm_mon-1} months, {time_obj.tm_mday-1} days'
        else:
            return today.year-birthdate.year

    class Meta:
        model = Pet
        fields = (
            # 'url',
            'owner',
            'name',
            'breed',
            'age',
            'images'
        )
