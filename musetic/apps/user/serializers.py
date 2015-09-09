from rest_framework import serializers

from musetic.apps.user.models import Profile, User, Creator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'is_staff')


class ProfileSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField('get_score')
    discussion_score = serializers.SerializerMethodField('get_discussion_score')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'description', 'score', 'discussion_score')

    user = UserSerializer()

    def get_score(self, obj):
        return obj.score()

    def get_discussion_score(self, obj):
        return obj.discussion_score()


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ('id', 'user', 'url', 'is_creator')

    user = UserSerializer()
