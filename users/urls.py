from django.urls import path
from users import views


urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('create/', views.RegistrationUserView.as_view(), name='register'),
    path('<int:pk>/update//password_change/', views.UserPasswordChangeView.as_view(), name='change_password'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(), name='update_user')
]
