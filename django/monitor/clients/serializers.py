from rest_framework import serializers
from .models import AlertsConfig
import yaml
from yamlfield.serializers import OrderedDumper

class AlertsConfigSerializer(serializers.ModelSerializer):

    yaml = serializers.SerializerMethodField()

    def get_yaml(self, obj):
        return yaml.dump(
            obj.yaml,
            Dumper=OrderedDumper,
            default_flow_style=False
        )

    class Meta:
        model = AlertsConfig
        fields = ['pk', 'title', 'yaml']
