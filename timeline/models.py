from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Timeline(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    name = models.fields.CharField(
        max_length=150,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Лента записей'
        verbose_name_plural = 'Ленты записей'

    def __str__(self):
        return f'{self.name}_{self.id}'


@receiver(post_save, sender=User)
def create_timeline(sender, instance, created, **kwargs):
    if created:
        Timeline.objects.create(
            name=f'Лента пользователя {instance.username}',
            user=instance,
        )