from rest_framework.permissions import BasePermission

from board.models import Moderator


class CustomPermissionClass(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            if not request.user.is_anonymous:
                return True
            else:
                return False
        elif request.method == 'PUT' or request.method == 'DELETE':
            if request.user:
                moderator = Moderator.objects.filter(moderator=request.user, board__id=view.kwargs.get('pk', 0))
                return True if moderator else False
        return False
