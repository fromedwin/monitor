from rest_framework import serializers

class PerfromanceSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    url = serializers.URLField()
    creation_date = serializers.DateTimeField()
