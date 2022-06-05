
from django.urls import path
from .views import RegisterView, LoginView, ProfileView,LogoutView, ProfileUpdateView, about, UsersView, UserProfileView


app_name='users'
urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('about/', about, name='about'),
    path('users/', UsersView.as_view(), name='users'),
    path('<int:id>/', UserProfileView.as_view(), name='userprofile'),

]

