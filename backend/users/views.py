from django.shortcuts import get_object_or_404

from rest_framework.filters import SearchFilter

from api.pagination import RecipesPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from djoser.serializers import SetPasswordSerializer

# from .permissions import IsAdmin
from users.models import User, Follow
from .serializers import UserSerializer
from api.serializers import FollowSerializer
from api.permissions import IsUserOrAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """Кастный Viewset для Пользователя."""

    queryset = User.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = UserSerializer
    pagination_class = RecipesPagination
    filter_backends = [SearchFilter]
    search_fields = ["username"]
    permission_classes = [IsUserOrAdminOrReadOnly]

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Показывает информацию о залогиненном пользователе."""
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def set_password(self, request, *args, **kwargs):
        """
        Кастомное изменение пароля
        """
        serializer = SetPasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data["new_password"])
            self.request.user.save()
            return Response(
                "Пароль успешно изменен", status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        """
        Показывает список подписок.
        """
        follows = Follow.objects.filter(user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, pk):
        """
        Подписка и отписка на автора.
        """
        author = get_object_or_404(User, id=pk)
        user = self.request.user
        if request.method == "POST":
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    "Пользователь уже подписан на этого Автора.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = FollowSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, author=author)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if not Follow.objects.filter(user=user, author=author).exists():
            return Response(
                "Пользователь не подписан на данного автора",
                status=status.HTTP_404_NOT_FOUND,
            )
        Follow.objects.get(user=user, author=author).delete()
        return Response(
            "Пользователь отписался от Автора.",
            status=status.HTTP_204_NO_CONTENT,
        )
