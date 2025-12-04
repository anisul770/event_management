from django.urls import path
from event.views import category_page,event_page,event_list,participant_page

urlpatterns = [
    path('categories/', category_page, name='category_page'),
    path('events/', event_page, name='event_page'),
    path('participants/', participant_page, name='participant_page'),
    path('event_list/',event_list,name='event-list')
]