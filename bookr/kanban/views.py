from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by('-timestamp')  # Order by timestamp descending
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@csrf_exempt  # handle CSRF differently in production
def update_task_status(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body)
        task.status = data['status']
        task.save()
        return JsonResponse({"message": "Task status updated successfully"}, status=200)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)