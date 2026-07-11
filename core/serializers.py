from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Category, Tag, Info

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', "username", "first_name", 'last_name')


class CommentSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True)
    # post = PostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['author'] = request.user
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user


class PostSerializer(serializers.ModelSerializer):
    # Avtordin toliq Magliwmatin korsetiw ushin
    author = UserSerializer(read_only = True)
    # comments = CommentSerializer(many=True, read_only=True)


    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'category', 'tags', 'author')

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     if request and request.user:
    #         validated_data['author'] = self.context['request'].user
    #     return super().create(validated_data)
    

    
class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('name', 'phone_number')

        