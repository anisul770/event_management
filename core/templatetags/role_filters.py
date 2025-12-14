from django import template

register = template.Library()

@register.filter
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@register.filter
def is_organizer(user):
    return user.groups.filter(name__in=['Organizer', 'Admin']).exists()

@register.filter
def is_participant(user):
    return user.groups.filter(name__in=['Participants','Organizer', 'Admin']).exists()

@register.filter
def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)