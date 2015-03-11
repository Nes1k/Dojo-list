from rest_framework import serializers

from .models import List, Action


class ListSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = List
        fields = ('owner', 'id', 'name',)

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=List.objects.all(),
                fields=('owner', 'name')
            )
        ]


class ActionSerializer(serializers.ModelSerializer):
    list = serializers.HiddenField(default=1)

    class Meta:
        model = Action
        fields = ('id', 'text', 'done', 'list')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Action.objects.all(),
                fields=('text', 'list'))
        ]
