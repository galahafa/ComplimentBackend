from rest_framework import serializers

from apps.models.tags import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
