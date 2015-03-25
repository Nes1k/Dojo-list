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
        if not queryset:
            List.objects.create(owner=request.user, name="Inbox")
        serializer = ListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        context = {'request': self.request}
        list_ = ListSerializer(data=request.data, context=context)
        if list_.is_valid():
            list_.save(owner=request.user)
            return Response(status=status.HTTP_201_CREATED, data=list_.data)
        else:
            return Response(list_.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(List, pk=pk)
        serializer = ListSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, pk=None):
        context = {'request': self.request}
        list_ = get_object_or_404(List, pk=pk)
        serializer = ListSerializer(
            data=request.data, instance=list_, context=context)
        if serializer.is_valid():
            serializer.save()
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
        list_ = get_object_or_404(List, pk=list_pk, owner=request.user)
        actions = Action.objects.filter(list=list_, list__owner=request.user)
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)

    def create(self, request, list_pk=None):
        list_ = get_object_or_404(List, pk=list_pk, owner=request.user)
        context = {'list': list_}
        serializer = ActionSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, list_pk=None, pk=None):
        action = get_object_or_404(Action, pk=pk,
                                   list__owner=request.user)
        serializer = ActionSerializer(action)
        return Response(serializer.data)

    def update(self, request, list_pk=None, pk=None):
        action = get_object_or_404(Action, pk=pk,
                                   list__owner=request.user)
        list_ = get_object_or_404(List, pk=list_pk, owner=request.user)
        context = {'list': list_}
        serializer = ActionSerializer(
            data=request.data, instance=action, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, list_pk=None,  pk=None):
        action = get_object_or_404(Action, pk=pk,
                                   list__owner=request.user)
        action.delete()
        return Response(status=status.HTTP_200_OK)
