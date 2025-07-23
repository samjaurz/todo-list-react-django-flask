from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def task(request, pk=None):
    if request.method == 'GET':
        if pk is None:
            tasks = Task.objects.all().order_by('id')
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        else:
            task = get_object_or_404(Task, pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        if pk is None:
            return Response({'error': 'Task ID is required'}, status=400)
        task_instance = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if pk is None:
            return Response({'error': 'Task ID is required'}, status=400)
        task_instance = get_object_or_404(Task, pk=pk)
        task_instance.delete()
        return Response(status=204)

    if request.method == 'GET':
        if pk is None:
            name = request.query_params.get('name')
            if name:
                tasks = Task.objects.filter(name__icontains=name)
            else:
                tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        else:
            task = get_object_or_404(Task, pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)