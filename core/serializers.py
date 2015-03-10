from rest_framework import serializers

from .models import List, Action


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id', 'name',)


class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = ('id', 'text', 'done', 'list')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Action.objects.all(),
                fields=('text', 'list'))
        ]
