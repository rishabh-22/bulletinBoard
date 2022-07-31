import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from user_auth.serializers import RegistrationSerializer


class Register(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """
        this function is used for registering a user into the system.
        :param request:
        :return:
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(self.request.data['password']))
            token, created = Token.objects.get_or_create(user=user)
            response = dict(message='successfully registered.', token=token.key)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

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

