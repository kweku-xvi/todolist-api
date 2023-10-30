from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TodoSerializer
from rest_framework import permissions, filters
from .models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageNumberPagination

# class CreateTodoAPIView(CreateAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def perform_create(self, serializer):
#         return serializer.save(owner=self.request.user)


# class TodoListAPIView(ListAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         return Todo.objects.filter(owner=self.request.user)


class TodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'title', 'is_complete']
    search_fields = ['id', 'title', 'description', 'is_complete']
    ordering_fields = ['id', 'title', 'description', 'is_complete']

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)