from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Account(User):
    user = models.OneToOneField(
        User,
        parent_link=True,
        on_delete=models.CASCADE
    )

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created and not instance.username == "admin":
        Account.objects.create(user=instance)

@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    try:
        Account.objects.get(user=instance).delete()
    except Account.DoesNotExist:
        pass


