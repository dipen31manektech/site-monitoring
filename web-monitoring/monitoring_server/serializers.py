from monitoring_server.models import exceptionDetails
from rest_framework import serializers


class ExceptionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = exceptionDetails
        fields = ['Request_URL', 'Exception_Location', 'Server_time', 'Exception_Type']
