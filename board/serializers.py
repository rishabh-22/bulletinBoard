from board.models import Board, Moderator, Post, Thread

from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['topic', 'context']


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = ['username', 'board_id']


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['board_id', 'text']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['thread_id', 'title', 'content']
