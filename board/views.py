import logging
import uuid

from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from board.models import Board, Thread, Post, Moderator
from board.serializers import BoardSerializer, ModeratorSerializer, PostSerializer, ThreadSerializer
from board.permissions import BoardPermissionClass, ThreadPermissionClass, PostPermissionClass, ModeratorPermissionClass


class BoardList(APIView):

    permission_classes = [BoardPermissionClass]

    def get(self, request):
        try:
            boards = Board.objects.all()
            response = [x.__dict__ for x in boards]
            [x.pop('_state') for x in response]
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
            thread = Thread.objects.get(board__id=pk)  # returns all the threads related to this board
            response = thread.__dict__
            response.pop('_state')
            return Response(response, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'message': 'no board with such id exists.'}, status=status.HTTP_404_NOT_FOUND)
        except Thread.DoesNotExist:
            return Response({'message': 'no threads for this board exist.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            board = Board.objects.get(id=pk)
            serializer = BoardSerializer(board, data=request.data)
            if serializer.is_valid():
                board = serializer.save(owner=request.user)
                response = dict(message=f'successfully modified board with id {board.id}.')
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Board.DoesNotExist:
            return Response({'message': 'no board with such id exists.'}, status=status.HTTP_404_NOT_FOUND)

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
    see all the posts related to a thread
    """
    permission_classes = [ThreadPermissionClass]

    def get(self, request):
        try:
            thread_id = request.data.get('thread_id')
            if thread_id is not None:
                posts = Post.objects.filter(thread__id=thread_id)
                response = [x.__dict__ for x in posts]
                [x.pop('_state') for x in response]
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'invalid thread id'}, status=status.HTTP_400_BAD_REQUEST)
        except Thread.DoesNotExist:
            return Response({'message': 'no thread found with this id'}, status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response({'message': 'no posts found for this thread id'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            board_id = request.data.get('board_id')
            if board_id is None:
                return Response({'message': 'invalid board id.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ThreadSerializer(data=request.data)
            if serializer.is_valid():
                uid = uuid.uuid4().hex
                board = Board.objects.get(id=board_id)
                thread = serializer.save(owner=request.user, board=board, id=uid)
                response = dict(message=f'successfully created thread with id {uid}.')
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Board.DoesNotExist:
            return Response({'message': 'no board with this id exists.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            thread_id = request.data.get('thread_id')
            thread_text = request.data.get('text')
            if thread_id is not None and thread_text is not None:
                thread = Thread.objects.get(id=thread_id)
                thread.text = thread_text
                thread.save()
                return Response({'message': 'thread text updated!'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'thread id or updated text is missing'}, status=status.HTTP_400_BAD_REQUEST)
        except Thread.DoesNotExist:
            return Response({'message': 'no thread with such id exists.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            thread_id = request.data.get('thread_id')
            if thread_id is not None:
                thread = Thread.objects.get(id=thread_id)
                thread.delete()
                return Response({'message': 'thread deleted!'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'thread id is missing'}, status=status.HTTP_400_BAD_REQUEST)
        except Thread.DoesNotExist:
            return Response({'message': 'no thread with such id exists.'}, status=status.HTTP_404_NOT_FOUND)


class PostList(APIView):
    """
    create new post
    """
    permission_classes = [PostPermissionClass]

    def get(self, request):
        try:
            posts = Post.objects.all()  # can change this to return all posts of a thread/board
            response = [x.__dict__ for x in posts]
            [x.pop('_state') for x in response]
            return Response(response, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'message': 'no post exists.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            thread_id = request.data.get('thread_id')
            if thread_id is None:
                return Response({'message': 'invalid thread id.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                thread = Thread.objects.get(id=thread_id)
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

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                post = serializer.save(author=request.user)
                response = dict(message=f'successfully modified post.')
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = serializer.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'message': 'no post with such id exists.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            post.delete()
            return Response({'message': f'post with id {pk} deleted successfully!'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'no post with such id exists.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(e)
            return Response({'message': 'some error occurred, please try again later.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ModeratorList(APIView):
    """
    handle moderator related stuff, sending and accepting/rejecting moderator request.
    """
    permission_classes = [ModeratorPermissionClass]

    def get(self, request):
        try:
            requests = Moderator.objects.filter(moderator=request.user, active=False)
            response = [x.__dict__ for x in requests]
            [x.pop('_state') for x in response]
            return Response(response, status=status.HTTP_200_OK)
        except Moderator.DoesNotExist:
            return Response({'message': 'no requests found for your account'})

    def post(self, request):
        try:
            username = request.data.get('username')
            board_id = request.data.get('board_id')
            if username is None or board_id is None:
                return Response({'message': 'please check the data you have sent. username and board_id is required.'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = ModeratorSerializer(data=request.data)
            if serializer.is_valid():
                moderator = User.objects.get(username=username)
                board = Board.objects.get(id=board_id)
                serializer.save(moderator=moderator, board=board)
                return Response({'message': 'moderator request successfully created.'}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'message': 'user with username not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Board.DoesNotExist:
            return Response({'message': 'board with id not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(e)
            return Response({'message': 'please check the data you have sent.'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            request_id = request.data.get('request_id')
            if request_id is None:
                return Response({'message': 'invalid request id!'}, status=status.HTTP_400_BAD_REQUEST)
            moderator_request = Moderator.objects.get(id=request_id)
            moderator_request.active = True
            moderator_request.save()
            return Response({'message': 'request accepted!'}, status=status.HTTP_200_OK)
        except Moderator.DoesNotExist:
            return Response({'message': 'invalid request id!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(e)
            return Response({'message': 'invalid data!'}, status=status.HTTP_403_FORBIDDEN)


class BoardGroup(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        result = Board.objects.values('topic').annotate(dcount=Count('topic')).order_by('topic')
        return Response(result, status=status.HTTP_200_OK)
        # response = []
        # result = Board.objects.raw('SELECT * FROM board_board group by board_board.topic')
        # for item in result:
        #     response.append(item)
        # return Response(response, status=status.HTTP_200_OK)
