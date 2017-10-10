from django.contrib.auth.models import User, Group
from rest_framework import serializers
from compile_server.app.models import Resource, Example


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ResourceSerializer(serializers.Serializer):
    class Meta:
        model = Resource
        fields = ('basename', 'code')

    contents = serializers.CharField(style={'base_template': 'textarea.html'})
    basename = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.contents = validated_data.get('contents', instance.contents)
        instance.basename = validated_data.get('basename', instance.basename)
        instance.save()
        return instance


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ('name', 'description', 'main')
