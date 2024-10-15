from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, F, functions


class User(AbstractUser):
    age = models.PositiveBigIntegerField(null=True, blank=True, default=1)
    friends = models.ManyToManyField(
        to="self",
        symmetrical=True, #Параметр symmentrical=True означает, что, когда user_1 добавляет в свой список друзей user_2, то и у user_2 в списке друзей появится user_1.
        blank=True,
    )


class Chat(models.Model):

    class Meta: # чтобы избежать создания дубликатов чата. берется пользователь с наибольшим id,также берется пользователь с наименьшим id, 
                #проверяется, нет ли в БД записи, с такими же наибольшим и наименьшим id.
        constraints = [ 
            UniqueConstraint(
                functions.Greatest(F('user_1'), F('user_2')),
                functions.Least(F('user_1'), F('user_2')),
                name="users_chat_unique",
            ),
        ]

    user_1 = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="chats_as_user1",
    )
    user_2 = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="chats_as_user2",
    )


class Message(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    created_at = models.DateTimeField(auto_now_add=True)