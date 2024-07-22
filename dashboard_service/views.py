# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay, TruncYear
from .models import BookingEvent
from .serializers import DashboardSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


class DashboardView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(name='hotel_id', description='ID of the hotel', required=True, type=int),
            OpenApiParameter(name='period', description='Period of the dashboard', required=True, type=str,
                             enum=['day', 'month', 'year']),
            OpenApiParameter(name='year', description='Year of the dashboard', required=True, type=int),
        ],
        responses={200: 'application/json'},
    )
    def get(self, request):
        serializer = DashboardSerializer(data=request.GET)
        if serializer.is_valid():
            hotel_id = serializer.validated_data['hotel_id']
            period = serializer.validated_data['period']
            year = serializer.validated_data['year']

            if period == 'month':
                bookings = BookingEvent.objects.filter(
                    hotel_id=hotel_id,
                    night_of_stay__year=year,
                    rpg_status=1
                ).annotate(
                    month=TruncMonth('timestamp')
                ).values('month').annotate(
                    bookings_count=Count('id')
                ).values('month', 'bookings_count').order_by('month')

            elif period == 'day':
                bookings = BookingEvent.objects.filter(
                    hotel_id=hotel_id,
                    night_of_stay__year=year,
                    rpg_status=1
                ).annotate(
                    day=TruncDay('timestamp')
                ).values('day').annotate(
                    bookings_count=Count('id')
                ).values('day', 'bookings_count').order_by('day')

            elif period == 'year':
                bookings = BookingEvent.objects.filter(hotel_id=hotel_id, night_of_stay__year=year).annotate(
                    year=TruncYear('night_of_stay')).values('year').annotate(count=Count('id'))

            else:
                return Response({'error': 'Invalid period'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(bookings, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
