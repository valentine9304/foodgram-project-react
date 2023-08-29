from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

USER = "user"
ADMIN = "admin"
ROLES = [
    (USER, "user"),
    (ADMIN, "admin"),
]


class User(AbstractUser):
    """Кастомизированная модель Пользователей."""

    username = models.CharField(
        max_length=150,
        verbose_name="Логин",
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"^[\w@.+-_]+$", message="Недопустимые символы."
            )
        ],
    )
    email = models.EmailField(
        max_length=254, verbose_name="E-mail", unique=True
    )
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    role = models.CharField(
        max_length=20, verbose_name="Роль", choices=ROLES, default="user"
    )
    password = models.CharField(max_length=150, verbose_name="Пароль")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "author"),
                name="Пользователь не может быть подписан сам на себя",
            ),
        ]
