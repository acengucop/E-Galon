from rest_framework import serializers
from .models import Depot

class DepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        fields = '__all__'
