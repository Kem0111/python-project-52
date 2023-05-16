from task_manager.labels.views import (LabelsView,
                                       CreateLabelView,
                                       UpdateLabelView,
                                       DeleteLabelView)
from django.urls import path

urlpatterns = [
    path('', LabelsView.as_view(), name='labels'),
    path('create/', CreateLabelView.as_view(), name='create_label'),
    path('<int:pk>/update/', UpdateLabelView.as_view(), name='update_label'),
    path('<int:pk>/delete/', DeleteLabelView.as_view(), name='delete_label')
]
