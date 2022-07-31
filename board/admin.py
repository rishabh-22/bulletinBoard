from django.contrib import admin

from board.models import Board, Moderator, Thread, Post

admin.site.register(Board)
admin.site.register(Moderator)
admin.site.register(Thread)
admin.site.register(Post)
