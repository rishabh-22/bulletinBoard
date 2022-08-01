import logging
import uuid

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from board.models import Board, Thread, Post, Moderator
from board.serializers import BoardSerializer, ModeratorSerializer, PostSerializer, ThreadSerializer
from board.permissions import BoardPermissionClass, ThreadPermissionClass, PostPermissionClass, ModeratorPermissionClass


class BoardList(APIView):

    permission_classes = [BoardPermissionClass]

    def get(self, request):
        try:
            response = Board.objects.all()
            return Response(response, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'message': 'no board exists.'}, status=status.HTTP_404_NOT_FOUND)

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
            response = Thread.objects.get(board__id=pk)  # returns all the threads related to this board
            return Response(response, status=status.HTTP_200_OK)
        except (Board.DoesNotExist, Thread.DoesNotExist):
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

    def get(self, request):
        try:
            thread_id = request.data.get('thread_id')
            if thread_id is not None:
                posts = Post.objects.get(thread__id=thread_id)
                return Response(posts, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'invalid thread id'}, status=status.HTTP_400_BAD_REQUEST)
        except (Thread.DoesNotExist, Post.DoesNotExist):
            return Response({'message': 'no thread with this id'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = ThreadSerializer(data=request.data)
            if serializer.is_valid():
                uid = uuid.uuid4().hex
                board = Board.objects.get(id=request.data.get('board_id'))
                thread = serializer.save(owner=request.user, board=board, id=uid)
                response = dict(message=f'successfully created thread with id {uid}.')
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Board.DoesNotExist:
            return Response({'message': 'no board with this id exists.'}, status=status.HTTP_404_NOT_FOUND)


class PostList(APIView):
    """
    create new post
    """
    permission_classes = [PostPermissionClass]

    def get(self, request):
        try:
            response = Post.objects.all()  # todo: change this to return all posts of a thread/board
            return Response(response, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'message': 'no post exists.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                thread = Thread.objects.get(id=request.data.get('thread_id'))
                post = serializer.save(author=request.user, thread=thread)
                response = dict(message=f'successfully created post.')
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Thread.DoesNotExist:
            return Response({'message': 'no thread with this id exists.'}, status=status.HTTP_404_NOT_FOUND)


class PostDetail(APIView):
    """
    view, edit, delete the post based on post id
    """
    permission_classes = [PostPermissionClass]


class ModeratorList(APIView):
    """
    handle moderator related stuff, sending and accepting/rejecting moderator request.
    """
    permission_classes = [ModeratorPermissionClass]

    def get(self, request):
        try:
            requests = Moderator.objects.get(moderator=request.user, active=False)
            return Response(requests, status=status.HTTP_200_OK)
        except Moderator.DoesNotExist:
            return Response({'message': 'no requests found for your account'})

    def post(self, request):
        try:
            serializer = ModeratorSerializer(request.data)
            if serializer.is_valid():
                moderator = User.objects.get(username=request.data.get('username'))
                board = Board.objects.get(id=request.data.get('board_id'))
                serializer.save(moderator=moderator, board=board)
                return Response({'message': 'moderator request successfully created.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({'message': 'please check the data you have sent.'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            moderator_request = Moderator.objects.get(id=request.data.get('request_id', 0))
            moderator_request.active = True
            moderator_request.save()

        except Moderator.DoesNotExist:
            return Response({'message': 'invalid request id!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(e)
            return Response({'message': 'invalid data!'}, status=status.HTTP_403_FORBIDDEN)
