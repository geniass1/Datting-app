from rest_framework import serializers
from user.models import NewUser
from .models import Messages, Likes


class UserMatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = (
            'username', 'email'
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = (
            'who', 'whom', 'message'
        )

    def create(self, validated_data):
        cr_message = Messages(
            who=validated_data['who'],
            whom=validated_data['whom'],
            message=validated_data['message']
        )
        new_message = Messages.objects.create(who=validated_data['who'], whom=validated_data['whom'],
                                              message=validated_data['message'])
        return new_message


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = (
            'who', 'whom',
        )

    def create(self, validated_data):
        like = Messages(
            who=validated_data['who'],
            whom=validated_data['whom'],
        )
        likes = Likes(who=validated_data['who'], whom=validated_data['whom'], is_liked=True)
        likes.save()
        return likes





