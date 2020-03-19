from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Account


class Blog(models.Model):
    name = models.fields.CharField(max_length=150, verbose_name='Название')
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=Account)
def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(
            name=f"Блог пользователя {instance.user.username}",
            account=instance,
        )
