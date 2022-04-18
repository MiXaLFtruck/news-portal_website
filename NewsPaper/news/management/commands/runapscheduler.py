import logging
from datetime import *
import pytz

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Category, Post

logger = logging.getLogger(__name__)


def my_job():
    #  Your job processing logic here...
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")