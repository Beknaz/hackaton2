from rest_framework import serializers
from django.shortcuts import get_object_or_404


from .models import Doctor, Comment, Rating, Favorite, Chat, Entry


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["comments"] = CommentSerializer(instance.comments.all(), many=True).data
        rep["likes"] = instance.likes.all().count()
        rep["rating"] = instance.average_rating
        request = self.context.get("request")
        if request.user.is_authenticated:
            if Rating.objects.filter(user=request.user, doctor=instance).exists():
                rating = Rating.objects.get(user=request.user, doctor=instance)
                rep["user_rating"] = rating.value
        return rep


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user']

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep  = super().to_representation(instance)
        rep["user"] = instance.user.username
        return rep


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        exclude = ['user']

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep  = super().to_representation(instance)
        rep["user"] = instance.user.username
        return rep


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        exclude = ['user']
    
    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep  = super().to_representation(instance)
        rep["user"] = instance.user.email
        return rep


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

    def create(self, validated_data):
        entry = super().create(validated_data)
        self.status(self.context.get('request'), entry.doctor.id)
        return entry


    def status(self, request, p_id):
        user = request.user
        doctor = get_object_or_404(Doctor, id=p_id)
        doctor.status = 1
        doctor.save()


    def to_representation(self, instance):
        rep = super().to_representation(instance)