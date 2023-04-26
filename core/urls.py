from django.urls import path
from core.views import HomePageView, LoginUserView, LogoutUserView


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='index')
]
