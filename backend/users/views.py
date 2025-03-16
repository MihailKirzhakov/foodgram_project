import os

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import FavoriteSerializer

from .models import Subscribe, UserProfile
from .serializers import AvatarSerializer


class UserProfileViewSet(viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()

    @action(
        methods=['PUT', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me/avatar'
    )
    def avatar(self, request):
        avatar_serializer = AvatarSerializer(
            request.user, data=request.data
        )
        avatar_serializer.context['request'] = request
        avatar_serializer.is_valid(raise_exception=True)
        avatar_serializer.save()
        return Response(avatar_serializer.data)

    @avatar.mapping.delete
    def del_avatar(self, request):
        user = request.user
        if user.avatar:
            os.remove(user.avatar.path)
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'У вас нет аватара'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['POST', 'GET'],
        permission_classes=[IsAuthenticated],
        detail=True,
    )
    def subscribe(self, request, pk=None):
        follower = request.user
        following = get_object_or_404(UserProfile, id=pk)

        if follower == following:
            return Response(
                data={'errors': 'Вы не можете подписываться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscribe.objects.filter(
            follower=follower, following=following,
        ).exists():
            return Response(
                data={'errors': 'Вы уже подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        subscribe = Subscribe.objects.create(
            follower=follower,
            following=following,
        )
        serializer = FavoriteSerializer(
            subscribe,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, pk=None):
        follower = request.user
        following = get_object_or_404(UserProfile, id=pk)

        subscribe = Subscribe.objects.filter(
            follower=follower,
            following=following,
        )
        if subscribe:
            subscribe.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )
        error_code = (
            'Нельзя подписаться на себя' if follower
            == following else 'Вы не подписаны на пользователя'
        )
        return Response(
            data={'errors': error_code},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follower = request.user
        queryset = Subscribe.objects.filter(follower=follower)
        pages = self.paginate_queryset(queryset)
        serializer = FavoriteSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
