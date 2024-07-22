# serializers.py
from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    period = serializers.ChoiceField(choices=['month', 'day', 'year'])
    hotel_id = serializers.IntegerField()
    year = serializers.IntegerField()
