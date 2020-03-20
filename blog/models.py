from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SubscribeByBlog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Подписка на блог'
        verbose_name_plural = 'Подписки на блоги'

    def __str__(self):
        return f"{self.user}_{self.created_at}"


class Blog(models.Model):
    name = models.fields.CharField(
        max_length=150,
        verbose_name='Название'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    subscribes_by_blog = models.ManyToManyField(
        SubscribeByBlog,
    )

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f"{self.name}"

    def subscribe_by_blog(self, current_user):
        return self.subscribes_by_blog.filter(user=current_user).first()


@receiver(post_save, sender=User)
def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(
            name=f"Блог пользователя {instance.username}",
            user=instance,
        )


class Record(models.Model):
    title = models.fields.CharField(
        max_length=150,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name='Блог',
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f"{self.title}"