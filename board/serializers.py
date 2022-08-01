from board.models import Board, Moderator, Post, Thread

from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['topic', 'context']


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = []  # todo: fix via logic


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['text']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']
