from .views import LoginView,RegisterView
from django.urls import path,include


urlpatterns = [
    path(r'api/auth/', include('knox.urls')),
     path('login/',LoginView.as_view()),
    path('signup/',RegisterView.as_view())
]