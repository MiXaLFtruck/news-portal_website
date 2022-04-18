from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, get_connection
from django.contrib.sites.models import Site
from .models import Post
from django.contrib.auth.models import User


@receiver(post_save, sender=Post)
def notify_subscribers_newpost(sender, instance, created, **kwargs):
    if created:
        categories = instance.category.all()
        for cat in categories:
            emails = []
            for user in cat.subscribers.all():
                html_content = render_to_string('new-post-in-category.html', {'title': instance.title,
                                                                              'text': instance.text, 'username':
                                                                                  user.username})
                msg = EmailMultiAlternatives(
                    subject=f"Новый пост в твоей любимой категории {cat.name}",
                    body="",
                    from_email='trk.olimp@mail.ru',
                    to=[user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                emails.append(msg)
                # msg.send()

            get_connection().send_messages(emails)

            # def send_mass_html_mail(subject, message, html_message, from_email, recipient_list):
            #     emails = []
            #     for recipient in recipient_list:
            #         email = EmailMultiAlternatives(subject, message, from_email, [recipient])
            #         email.attach_alternative(html_message, 'text/html')
            #         emails.append(email)
            #     return get_connection().send_messages(emails)

@receiver(post_save, sender=User)
def new_user_greetings(sender, instance, created, **kwargs):
    if created:
        current_site = 'http://' + Site.objects.get_current().domain + ':8000/news/'
        html_content = render_to_string('email/new_user_greetings.html', {'username': instance.username,
                                                                          'site_domain': current_site})
        msg = EmailMultiAlternatives(
            subject=f"{instance.username}, приветствуем тебя на нашем сайте!",
            body="",
            from_email='trk.olimp@mail.ru',
            to=[instance.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
