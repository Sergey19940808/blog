from celery import shared_task
from django.core.mail import send_mail

from core.settings import EMAIL_HOST_USER


@shared_task
def send_notify(record_id, blog_id):
	from blog.models import Blog
	blog = Blog.objects.get(id=blog_id)
	own_record = blog.user
	blog = blog
	subscribes_by_blog = blog.subscribes_by_blog.all()

	for subscribe_by_blog in subscribes_by_blog:
		own_subscribe_record = subscribe_by_blog.timeline.user
		if own_subscribe_record.email and own_record.email:
			subject = f'Добавление новой записи в блог - {blog.name}'
			msg = f'Пользователь - {own_record.username}, добавил в блог - {blog.name}, '\
				  f'пост: http://localhost:8000/blog/{blog.id}/record/{record_id}'
			send_msg.delay(
				subject,
				msg,
				own_subscribe_record.email,
			)
		# When user has not email, going next
		else:
			continue


@shared_task
def send_msg(subject, msg, recipient):
	send_mail(
		subject,
		msg,
		EMAIL_HOST_USER,
		[recipient],
		False,
	)
