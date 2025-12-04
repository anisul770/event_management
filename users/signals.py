from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save,sender=User)
def send_activation_mail(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        message = f"Hi {instance.first_name}\n Please click this link to activate your account:\n {settings.FRONTEND_URL}/users/activate/{instance.id}/{token}  \n Thanks"
        subject = "Activate Your Account"
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER,[instance.email])
        except Exception as e:
            print(f"Failed to send email to {instance.email}")