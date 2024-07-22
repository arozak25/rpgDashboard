from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import BookingEvent


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('dashboard')

        # Create some test data
        BookingEvent.objects.create(id=1, hotel_id=1, timestamp='2023-01-01T12:00:00Z', rpg_status=1, room_id=101,
                                    night_of_stay='2023-01-01T00:00:00Z', updated='2023-01-01T12:00:00Z')
        BookingEvent.objects.create(id=2, hotel_id=1, timestamp='2023-01-02T12:00:00Z', rpg_status=1, room_id=101,
                                    night_of_stay='2023-01-02T00:00:00Z', updated='2023-01-02T12:00:00Z')

    @patch('requests.get')
    def test_dashboard_view(self, mock_get):
        # Mock the response from the data provider
        mock_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "hotel_id": 1,
                    "rpg_status": 1,
                    "room_id": 101,
                    "night_of_stay": "2023-01-01T00:00:00Z",
                    "updated": "2023-01-01T12:00:00Z"
                },
                {
                    "id": 2,
                    "hotel_id": 1,
                    "rpg_status": 1,
                    "room_id": 101,
                    "night_of_stay": "2023-01-02T00:00:00Z",
                    "updated": "2023-01-02T12:00:00Z"
                }
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Test the monthly period
        response = self.client.get(self.url, {'hotel_id': 1, 'period': 'month', 'year': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting a single entry for the month

        # Test the daily period
        response = self.client.get(self.url, {'hotel_id': 1, 'period': 'day', 'year': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting two entries for the days

        # Test the yearly period
        response = self.client.get(self.url, {'hotel_id': 1, 'period': 'year', 'year': 2023})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting a single entry for the year

    @patch('requests.get')
    def test_dashboard_view_invalid_params(self, mock_get):
        # Test missing parameters
        response = self.client.get(self.url, {'hotel_id': 1, 'period': 'month'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.url, {'hotel_id': 1, 'year': 2023})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.url, {'period': 'month', 'year': 2023})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid parameters
        response = self.client.get(self.url, {'hotel_id': 'invalid', 'period': 'month', 'year': 2023})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.url, {'hotel_id': 1, 'period': 'invalid', 'year': 2023})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(self.url, {'hotel_id': 1, 'period': 'month', 'year': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
