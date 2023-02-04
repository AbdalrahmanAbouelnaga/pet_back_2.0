from django.db import models
from uuid import uuid4
from PIL import Image
from io import BytesIO
from django.core.files import File
from django_extensions.db.models import AutoSlugField
from user.models import Profile


class Kind(models.Model):
    name = models.CharField(max_length=100,unique=True,primary_key=True)


    def __str__(self):
        return self.name



class Breed(models.Model):
    name = models.CharField(max_length=100,unique=True,primary_key=True)
    kind = models.ForeignKey(Kind,related_name='breeds',on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Pet(models.Model):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=['owner','name'])
    owner = models.ForeignKey(Profile,related_name='pets',on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed,related_name='pets',on_delete=models.CASCADE)
    birth_date = models.DateField()


    def __str__(self):
        return self.name



class PetImages(models.Model):
    pet = models.ForeignKey(Pet,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/',null=True,blank=True)


    def make_thumbnail(self):
        img = Image.open(self.image)
        img.convert('RGB')
        img.thumbnail(size=(400,400))

        thumb_io = BytesIO()

        img.save(thumb_io,'JPEG',quality=95,optimize=True)

        thumbnail = File(thumb_io,name=self.image.name)

        self.thumbnail = thumbnail

    def save(self) -> None:
        self.make_thumbnail()
        return super(PetImages,self).save()