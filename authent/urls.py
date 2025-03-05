from django.urls import path
from . import views
urlpatterns=[
    path('register',views.Register,name='register'),
    path('login',views.Login,name='login'),
    path('logout',views.Logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('changepassword',views.changepassword,name='changepassword'),
    
]