from . import views

from rest_framework_extensions.routers import ExtendedDefaultRouter


from django.urls import path


urlpatterns = [
    path('pets/',views.PetViewset.as_view()),
    path('kinds/',views.KindViewSet.as_view({'get':'list'}),name='kind-list'),
    path(r'kinds/<str:name>/',views.KindViewSet.as_view({'get':'retrieve'}),name='kind-detail'),
    path(r'kinds/<str:parent_lookup_kind>/breeds/',views.BreedViewset.as_view({'get':'list'}),name='breed-list'),
    path(r'kinds/<str:parent_lookup_kind>/breeds/<str:name>/',views.BreedViewset.as_view({'get':'retrieve'}),name='breed-detail'),
]