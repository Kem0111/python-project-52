from django.urls import path
from labels.views import (LabelsView,
                          CreateStatusView,
                          UpdateLabelView,
                          DeleteLabelView)

urlpatterns = [
    path('', LabelsView.as_view(), name='labels'),
    path('create/', CreateStatusView.as_view(), name='create_label'),
    path('<int:pk>/update/', UpdateLabelView.as_view(), name='update_label'),
    path('<int:pk>/delete/', DeleteLabelView.as_view(), name='delete_label')
]
