# test_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import BookingEvent
from django.utils import timezone


class DashboardAPITestCase(APITestCase):
    def setUp(self):
        # Set up initial data
        self.hotel_id = 1
        self.year = 2023
        self.month = 6
        self.day = 15

        BookingEvent.objects.create(
            id=1,
            hotel_id=self.hotel_id,
            timestamp=timezone.now(),
            rpg_status=1,
            room_id=101,
            night_of_stay=timezone.datetime(self.year, self.month, self.day),
            updated=timezone.now()
        )

        BookingEvent.objects.create(
            id=2,
            hotel_id=self.hotel_id,
            timestamp=timezone.now(),
            rpg_status=1,
            room_id=102,
            night_of_stay=timezone.datetime(self.year, self.month, self.day + 1),
            updated=timezone.now()
        )

    def test_dashboard_monthly(self):
        url = reverse('dashboard')
        response = self.client.get(url, {'hotel_id': self.hotel_id, 'period': 'month', 'year': self.year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('month' in response.json()[0])
        self.assertTrue('bookings_count' in response.json()[0])

    def test_dashboard_daily(self):
        url = reverse('dashboard')
        response = self.client.get(url, {'hotel_id': self.hotel_id, 'period': 'day', 'year': self.year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('day' in response.json()[0])
        self.assertTrue('bookings_count' in response.json()[0])

    def test_dashboard_missing_parameters(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dashboard_invalid_period(self):
        url = reverse('dashboard')
        response = self.client.get(url, {'hotel_id': self.hotel_id, 'period': 'invalid', 'year': self.year})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
