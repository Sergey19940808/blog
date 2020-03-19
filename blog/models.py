from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Blog(models.Model):
    name = models.fields.CharField(
        max_length=150,
        verbose_name='Название'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f"{self.name}"

@receiver(post_save, sender=User)
def create_blog(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Blog.objects.create(
            name=f"Блог пользователя {instance.username}",
            user=instance,
        )
