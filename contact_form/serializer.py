from rest_framework import serializers


class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    number = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()