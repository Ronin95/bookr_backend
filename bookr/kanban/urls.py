from django.urls import path
from .views import TaskListCreateView, TaskDetailView, update_task_status

urlpatterns = [
    # ... your other url patterns
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/update-status/<int:task_id>/', update_task_status, name='update_task_status'),
]
