import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_files.settings')

app = Celery('project_files')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# еженедельная рассылка о постах за неделю подписчикам в категории
app.conf.beat_schedule = {
    'notify_subscribers_every_monday_8am': {
        'task': 'news.tasks.notify_subscribers',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
