from django import forms
from event.models import Event, Participant, Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'participants','category']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name','last_name', 'email']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
