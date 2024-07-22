# tasks.py
import requests
import logging
from celery import shared_task
from django.utils.dateparse import parse_datetime
from .models import BookingEvent
from django.db import IntegrityError

logger = logging.getLogger(__name__)


@shared_task(name="fetch_and_save_booking_events")
def fetch_and_save_booking_events():
    url = 'http://localhost:8001/api/events/'
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to fetch data from {url}, status code: {response.status_code}")
            break

        data = response.json()
        for event in data['results']:
            try:
                # Check if the record already exists
                booking_event, created = BookingEvent.objects.get_or_create(
                    id=event['id'],
                    defaults={
                        'hotel_id': event['hotel_id'],
                        'timestamp': parse_datetime(event['updated']),
                        'rpg_status': event['rpg_status'],
                        'room_id': event['room_id'],
                        'night_of_stay': parse_datetime(event['night_of_stay']),
                        'updated': parse_datetime(event['updated']),
                    }
                )
                if not created:
                    # Update the existing record
                    booking_event.hotel_id = event['hotel_id']
                    booking_event.timestamp = parse_datetime(event['updated'])
                    booking_event.rpg_status = event['rpg_status']
                    booking_event.room_id = event['room_id']
                    booking_event.night_of_stay = parse_datetime(event['night_of_stay'])
                    booking_event.updated = parse_datetime(event['updated'])
                    booking_event.save()

                logger.info(f"{'Created' if created else 'Updated'} BookingEvent: {booking_event.id}")
            except IntegrityError as e:
                logger.error(f"IntegrityError for event ID {event['id']}: {e}")
            except Exception as e:
                logger.error(f"Error saving event ID {event['id']}: {e}")

        # Proceed to the next page, if available
        url = data.get('next')
