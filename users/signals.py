from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from event.models import Event
from django.db.models.signals import m2m_changed

@receiver(post_save,sender=User)
def send_activation_mail(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        message = f"Hi {instance.first_name}\n\n Please click this link to activate your account:\n {settings.FRONTEND_URL}/users/activate/{instance.id}/{token}  \n\n if you have not set any password please use 12345 \n\n Thanks"
        subject = "Activate Your Account"
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER,[instance.email])
        except Exception as e:
            print(f"Failed to send email to {instance.email}")

@receiver(m2m_changed, sender=Event.participants.through)
def send_event_confirmation_email(sender, instance, action, reverse, pk_set, **kwargs):
    # Fire only when a user is added
    if action == "post_add" and not reverse:
        # pk_set will contain exactly ONE user id since you add one user at a time
        user_id = next(iter(pk_set))  # extract the single user id
        user = User.objects.get(id=user_id)
        subject = f"You are going to: {instance.name}"
        message = (
            f"Hello {user.username},\n\n"
            f"Your response to the event '{instance.name}' has been recorded.\n\n"
            f"Event Details:\n"
            f"- Date: {instance.date}\n"
            f"- Time: {instance.time}\n\n"
            f"Thank you for your interest!\n"
        )
        send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False,)

            
