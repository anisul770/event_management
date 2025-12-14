from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from event.models import Event
from django.db.models.signals import m2m_changed
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(m2m_changed, sender=Event.participants.through)
def send_event_confirmation_email(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add":
        # If reverse=True → editing user.events
        if reverse:
            # instance is user, pk_set contains event ID(s)
            event_id = next(iter(pk_set))
            event = Event.objects.get(id=event_id)
            user = instance  # because reverse=True = user
        else:
            # Normal case: editing event.participants
            user_id = next(iter(pk_set))
            user = User.objects.get(id=user_id)
            event = instance  # event instance
        subject = f"You are going to: {event.name}"
        message = (
            f"Hello {user.username},\n\n"
            f"Your response to the event '{event.name}' has been recorded.\n\n"
            f"Event Details:\n"
            f"- Date: {event.date}\n"
            f"- Time: {event.time}\n\n"
            f"Thank you for your interest!\n"
        )
        send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=False,)

            
