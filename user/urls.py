from .views import LoginView,RegisterView,UserInfo,UpdateInfo,ChangePassword
from django.urls import path,include
from knox import views as knox_views


urlpatterns = [
    path(r'api/auth/', include('knox.urls')),
     path('login/',LoginView.as_view()),
    path('signup/',RegisterView.as_view()),
    path('user/',UserInfo.as_view()),
    path('user/update/',UpdateInfo.as_view()),
    path('user/pass-change/',ChangePassword.as_view()),
    path('logout/',knox_views.LogoutView.as_view(),name="logout"),
    path('logout/all/',knox_views.LogoutAllView.as_view(),name="logout-all")
]