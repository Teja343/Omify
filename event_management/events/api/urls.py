from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RegisterAttendeeView, EventAttendeesListView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path('events/<int:event_id>/register/', RegisterAttendeeView.as_view(), name='register-attendee'),
    path('events/<int:event_id>/attendees/', EventAttendeesListView.as_view(), name='event-attendees'),
]