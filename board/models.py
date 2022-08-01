from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Board(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    context = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.topic


class Moderator(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.board}-{self.moderator}'

    class Meta:
        unique_together = ('board', 'moderator',)


class Thread(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.id

    class Meta:
        unique_together = ('board', 'owner',)


class Post(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    author = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, unique=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Board)
def create_board_moderator(sender, instance=None, created=False, **kwargs):
    if created:
        Moderator.objects.create(board=instance, moderator=instance.owner, active=True)
