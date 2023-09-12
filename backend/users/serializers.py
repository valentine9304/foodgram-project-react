from rest_framework import serializers

from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_subscribed": {"read_only": True},
        }

    def create(self, validated_data):
        """
        Хэширует пароль.Так как без этого AuthToken не может считать его.
        """
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def get_is_subscribed(self, obj) -> bool:
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False

        return Follow.objects.filter(user=request.user, author=obj.id).exists()
