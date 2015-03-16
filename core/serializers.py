from rest_framework import serializers

from .models import List, Action


class ListSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    todo = serializers.IntegerField(read_only=True)

    class Meta:
        model = List
        fields = ('owner', 'id', 'name', 'todo')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=List.objects.all(),
                fields=('owner', 'name')
            )
        ]


class ActionSerializer(serializers.ModelSerializer):
    list = serializers.HiddenField(default=1)

    def validate_list(self, value):
        try:
            list_ = self.context['list']
            value = list_
        finally:
            return value

    class Meta:
        model = Action
        fields = ('id', 'text', 'done', 'list')

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Action.objects.all(),
                fields=('text', 'list'))
        ]
