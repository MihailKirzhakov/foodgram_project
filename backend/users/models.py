from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.constants import ProjectConstants


class UserProfile(AbstractUser):

    first_name = models.CharField(
        'Имя',
        max_length=ProjectConstants.USER_NAME_MAX_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=ProjectConstants.USER_LASTNAME_MAX_LENGTH
    )
    email = models.EmailField('Электронная почта', unique=True)
    avatar = models.ImageField(
        upload_to='users/images/',
        default=None,
        verbose_name='Аватарка',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')


class Subscribe(models.Model):
    follower = models.ForeignKey(
        UserProfile,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=models.CASCADE
    )

    following = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'follower'],
                name='unique follow',
            ),
            models.CheckConstraint(
                check=~models.Q(following=models.F('follower')),
                name='no_self_subscription'
            )
        ]
