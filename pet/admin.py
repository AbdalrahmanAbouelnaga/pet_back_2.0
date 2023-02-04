from django.contrib import admin
from .models import Pet,PetImages,Kind,Breed
# Register your models here.

admin.site.register(Kind)
admin.site.register(Breed)


class PetInline(admin.TabularInline):
    model = PetImages


class PetAdmin(admin.ModelAdmin):
    model = Pet
    inlines =(
        PetInline,
    )

admin.site.register(Pet,PetAdmin)