from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from events.models import Events, Attendee
from .serializers import AttendeeSerializer,EventSerializer
from events.api.services.registration_service import register_attendee
from django.utils.timezone import now


class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        return Events.objects.filter(start_time__gte=now()).order_by('start_time')

class RegisterAttendeeView(APIView):
    def post(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)
        name = request.data.get('name')
        email = request.data.get('email')

        if not name or not email:
            return Response({'error': 'Name and email are required.'}, status=400)

        success, message = register_attendee(event, name, email)
        if success:
            return Response({'message': 'Registration successful.'})
        return Response({'error': message}, status=400)

class EventAttendeesListView(APIView):
    def get(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)
        attendees = event.attendees.all().order_by('-id')
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(attendees, request)
        serializer = AttendeeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)