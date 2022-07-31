import logging
import uuid

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from board.models import Board
from board.serializers import BoardSerializer
from board.permissions import BoardPermissionClass, ThreadPermissionClass, PostPermissionClass


class BoardList(APIView):

    permission_classes = [BoardPermissionClass]

    def get(self, request):
        try:
            response = Board.objects.all()
            return Response(response, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'message': 'no board with such id exists.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            uid = uuid.uuid4().hex
            board = serializer.save(owner=request.user, id=uid)
            response = dict(message=f'successfully created board with id {uid}.')
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class BoardDetail(APIView):

    permission_classes = [BoardPermissionClass]

    def get(self, request, pk):
        try:
            response = Board.objects.get(id=pk)  # todo: change and try to return all the threads related to this board
            return Response(response, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'message': 'no board with such id exists.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        board = Board.objects.get(id=pk)
        serializer = BoardSerializer(board, data=request.data)
        if serializer.is_valid():
            board = serializer.save(owner=request.user)
            response = dict(message=f'successfully modified board with id {board.id}.')
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            board = Board.objects.get(id=pk)
            board.delete()
            return Response({'message': f'board with id {pk} deleted successfully!'}, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'message': 'no board with such id exists.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(e)
            return Response({'message': 'some error occurred, please try again later.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ThreadDetail(APIView):
    """
    minimum one pk is required, you can't see all threads and related posts. hence pk is mandatory, no need to create a
     thread, only refer a thread, thread creation will be automatic based on post creation without a thread id

    # todo: see all the posts related to a thread
    """
    permission_classes = [ThreadPermissionClass]


class PostList(APIView):
    """
    create new post
    """
    permission_classes = [PostPermissionClass]


class PostDetail(APIView):
    """
    view, edit, delete the post based on post id
    """
    permission_classes = [PostPermissionClass]


class Moderator(APIView):
    """
    handle moderator related stuff, sending and accepting/rejecting moderator request.
    """
    pass
