from celery import shared_task
from news.models import Category, Post
from datetime import *
import pytz
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# еженедельная рассылка о постах за неделю подписчикам на категорию
@shared_task
def notify_subscribers():
    categories = Category.objects.all()

    for cat in categories:
        recipients = []
        posts_to_send = Post.objects.filter(posted__gte=datetime.now(pytz.utc) - timedelta(days=7), category=cat)
        for user in cat.subscribers.all():
            recipients.append(user.email)

        if posts_to_send:
            html_content = render_to_string('email/new_posts_weekly.html', {'posts_to_send': posts_to_send, 'category':
                cat.name})
            msg = EmailMultiAlternatives(
                subject=f"Посты за неделю в твоей любимой категории {cat.name}",
                body="",
                from_email='trk.olimp@mail.ru',
                to=recipients
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
