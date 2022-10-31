from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)


class Subscriptions(models.Model):
    """Subscription model."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
        related_name="subscribers",
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Subscriber"),
        related_name="subscriptions",
    )

    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")

    def __str__(self):
        return f"{self.subscriber} subscribed to {self.author}"
