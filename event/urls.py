from django.urls import path
from event import views

urlpatterns = [
    path('categories/', views.category_page, name='category_page'),
    path('events/', views.event_page, name='event_page'),
    path('participants/', views.participant_page, name='participant_page'),
]