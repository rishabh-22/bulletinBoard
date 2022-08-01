from rest_framework.permissions import BasePermission

from board.models import Moderator, Board, Post, Thread


class BoardPermissionClass(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        elif request.method == 'POST':
            if not request.user.is_anonymous:
                return True

        elif request.method == 'PUT' or request.method == 'PATCH':
            if request.user:
                moderator = Moderator.objects.filter(moderator=request.user, board__id=view.kwargs.get('pk', 0),
                                                     active=True)
                return True if moderator else False

        elif request.method == 'DELETE':
            if request.user:
                try:
                    board = Board.objects.get(id=view.kwargs.get('pk', 0))
                    if board.owner == request.user:
                        return True
                except Board.DoesNotExist:
                    return True

        return False


class ThreadPermissionClass(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        elif request.method == 'POST':
            if not request.user.is_anonymous:
                return True

        elif request.method == 'PUT' or request.method == 'PATCH':
            if request.user:
                try:
                    thread = Thread.objects.get(id=view.kwargs.get('pk', 0))
                    moderator = Moderator.objects.filter(moderator=request.user, board__id=thread.board_id, active=True)
                    return True if moderator else False
                except Thread.DoesNotExist:
                    return True

        elif request.method == 'DELETE':
            if request.user:
                try:
                    thread = Thread.objects.get(id=view.kwargs.get('pk', 0))
                    if thread.owner == request.user:
                        return True
                except Board.DoesNotExist:
                    return True

        return False


class PostPermissionClass(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        elif request.method == 'POST':
            if not request.user.is_anonymous:
                return True

        elif request.method == 'PUT' or request.method == 'PATCH':
            if request.user:
                try:
                    post = Post.objects.get(id=view.kwargs.get('pk', 0))
                    moderator = Moderator.objects.filter(moderator=request.user, board__id=post.thread.board_id,
                                                         active=True)
                    return True if moderator else False
                except Post.DoesNotExist:
                    return True

        elif request.method == 'DELETE':
            if request.user:
                try:
                    post = Post.objects.get(id=view.kwargs.get('pk', 0))
                    if post.owner == request.user:
                        return True
                except Board.DoesNotExist:
                    return True

        return False


class ModeratorPermissionClass(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if not request.user.is_anonymous:
                return True

        elif request.method == 'POST':
            if not request.user.is_anonymous:
                try:
                    board = Board.objects.get(id=view.kwargs.get('board_id', 0))
                    if request.user == board.owner:
                        return True
                except Board.DoesNotExist:
                    return True

        elif request.method == 'PUT':
            if not request.user.is_anonymous:
                try:
                    moderator_request = Moderator.objects.get(id=view.kwargs.get('board_id', 0))
                    if moderator_request.moderator == request.user:
                        return True
                except Moderator.DoesNotExist:
                    return True

        return False
