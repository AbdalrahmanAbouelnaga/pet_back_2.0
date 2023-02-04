from django.db import models

from django.contrib.auth.models import AbstractUser,UserManager

from io import BytesIO
from PIL import Image 
from django.core.files import File
from uuid import uuid4

class Profile(AbstractUser):
    id = models.UUIDField(default=uuid4,primary_key=True,editable=False)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/',null=True,blank=True,)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name','last_name','email','image')


    def make_thumbnail(self):
        img = Image.open(self.image)
        img.convert('RGB')
        img.thumbnail(size=(400,400))

        thumb_io = BytesIO()

        img.save(thumb_io,'JPEG',quality=95,optimize=True)

        thumbnail = File(thumb_io,name=self.image.name)

        self.thumbnail = thumbnail

    def save(self,*args,**kwargs) -> None:
        if self.image:
            if not self.thumbnail:
                self.make_thumbnail()
        return super().save(*args,**kwargs)