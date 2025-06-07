from django.urls import reverse
from rest_framework.test import APITestCase
from events.models import Events
from django.utils import timezone
from datetime import timedelta

class RegisterAttendeeTest(APITestCase):
    def setUp(self):
        self.event = Events.objects.create(
            name="Classical Event",
            location="Hyderabad",
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=3),
            max_capacity=50
        )
        self.url = f'/api/events/{self.event.id}/register/'

    def test_register_attendee_success(self):
        response = self.client.post(self.url, {
            "name": "Krishna",
            "email": "Krishna@gmail.com"
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Registration successful.')

    def test_register_duplicate_email(self):
        self.client.post(self.url, {
            "name": "Sai",
            "email": "saiteja@gmail.com"
        }, format='json')
        response = self.client.post(self.url, {
            "name": "Sai",
            "email": "saiteja@gmail.com"
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'This email is already registered for the event.')
