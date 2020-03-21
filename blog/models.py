import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from timeline.models import Timeline


# Models
class SubscribeRecord(models.Model):
    is_read = models.BooleanField(
        default=False,
        verbose_name='Запись прочитана пользователем'
    )
    record = models.OneToOneField(
        'blog.Record',
        on_delete=models.CASCADE,
        verbose_name='Запись',
    )

    class Meta:
        verbose_name = 'Запись из блога на которую подписан пользователь'
        verbose_name_plural = 'Записи из блога на которую подписан пользователь'

    def __str__(self):
        return f'{self.id}'


class SubscribeByBlog(models.Model):
    timeline = models.ForeignKey(
        'timeline.Timeline',
        on_delete=models.CASCADE,
        verbose_name='Лента записей'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    subscribes_record = models.ManyToManyField(
        'blog.SubscribeRecord',
        verbose_name='Подписка на новость',
    )

    class Meta:
        verbose_name = 'Подписка на блог'
        verbose_name_plural = 'Подписки на блоги'

    def __str__(self):
        return f'{self.created_at}'


class Blog(models.Model):
    name = models.fields.CharField(
        max_length=150,
        verbose_name='Название'
    )
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    subscribes_by_blog = models.ManyToManyField(
        'blog.SubscribeByBlog',
        verbose_name='Подписки на блог',
    )

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f'{self.name}'


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
        'blog.Blog',
        on_delete=models.CASCADE,
        verbose_name='Блог',
    )

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return f'{self.title}'


# Signals for models
@receiver(post_save, sender=User)
def create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(
            name=f'Блог пользователя {instance.username}',
            user=instance,
        )


@receiver(post_save, sender=Record)
def create_subscribe_record(sender, instance, created, **kwargs):
    from manager_tasks.tasks import send_notify
    if created:
        subscribes_by_blog = instance.blog.subscribes_by_blog.all()
        if subscribes_by_blog:
            send_notify.delay(instance.id, instance.blog.id)
            for subscribe_by_blog in subscribes_by_blog:
                subscribe_by_blog.subscribes_record.add(SubscribeRecord.objects.create(record=instance))


@receiver(post_delete, sender=Record)
def delete_subscribe_record(sender, instance, **kwargs):
    subscribes_by_blog = instance.blog.subscribes_by_blog.all()
    if subscribes_by_blog:
        for subscribe_by_blog in subscribes_by_blog:
            subscribe_by_blog.subscribes_record.filter(record=instance).delete()