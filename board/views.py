import logging
import uuid

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from board.models import Board
from board.permissions import CustomPermissionClass
from board.serializers import BoardSerializer


class BoardList(APIView):

    permission_classes = [CustomPermissionClass]

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

    permission_classes = [CustomPermissionClass]

    def get(self, request, pk):
        try:
            response = Board.objects.get(id=pk)
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
            # logging.log(e)
            return Response({'message': 'some error occurred, please try again later.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ThreadList(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        this function is used for returning an auth token to a valid user.
        :param request:
        :return:
        """
        try:
            user = User.objects.get(username=request.data['username'])
            if not user.check_password(request.data['password']):
                raise Exception
            token, created = Token.objects.get_or_create(user=user)
            response = dict(message='login successful.', token=token.key)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            logging.debug(e)
            return Response({
                'error': 'provided data is incorrect.'
            }, status=status.HTTP_400_BAD_REQUEST)

