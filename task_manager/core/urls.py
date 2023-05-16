from django.urls import path, include
from task_manager.core.views import HomePageView, LoginUserView, LogoutUserView


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('', HomePageView.as_view(), name='index'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls'))
]
