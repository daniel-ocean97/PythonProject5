from rest_framework import serializers

def validate_url(value):
    youtube = 'youtube.com'
    if youtube not in value:
        raise serializers.ValidationError("Here must be youtube video")
