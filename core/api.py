from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ListSerializer, ActionSerializer
from .models import List, Action


class ListViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = List.objects.filter(owner=request.user)
        serializer = ListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        list_ = ListSerializer(data=request.data)
        if list_.is_valid():
            list_.save(owner=request.user)
            return Response(list_.data)
        else:
            return Response(list_.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(List, pk=pk)
        serializer = ListSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        list_ = get_object_or_404(List, pk=pk)
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            list_.name = serializer.data.get('name')
            list_.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        list_ = get_object_or_404(List, pk=pk)
        list_.delete()
        return Response(status=status.HTTP_200_OK)


class ActionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, list_pk=None):
        actions = Action.objects.filter(list=list_pk)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

    def create(self, request, list_pk=None):
        serializer = ActionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, list_pk=None, pk=None):
        action = get_object_or_404(Action, pk=pk)
        serializer = ActionSerializer(action)
        return Response(serializer.data)

    def update(self, request, list_pk=None, pk=None):
        action = get_object_or_404(Action, pk=pk)
        serializer = ActionSerializer(data=request.data, instance=action)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, list_pk=None,  pk=None):
        action = get_object_or_404(Action, pk=pk)
        action.delete()
        return Response(status=status.HTTP_200_OK)
