# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncDay
from .models import BookingEvent
from .serializers import DashboardSerializer


class DashboardView(APIView):

    def get(self, request):
        serializer = DashboardSerializer(data=request.GET)
        if serializer.is_valid():
            hotel_id = serializer.validated_data['hotel_id']
            period = serializer.validated_data['period']
            year = serializer.validated_data['year']

            if period == 'month':
                bookings = BookingEvent.objects.filter(
                    hotel_id=hotel_id,
                    night_of_stay__year=year
                ).annotate(
                    month=TruncMonth('night_of_stay')
                ).values('month').annotate(
                    bookings_count=Count('id')
                ).values('month', 'bookings_count').order_by('month')

            elif period == 'day':
                bookings = BookingEvent.objects.filter(
                    hotel_id=hotel_id,
                    night_of_stay__year=year
                ).annotate(
                    day=TruncDay('night_of_stay')
                ).values('day').annotate(
                    bookings_count=Count('id')
                ).values('day', 'bookings_count').order_by('day')

            return Response(bookings, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
