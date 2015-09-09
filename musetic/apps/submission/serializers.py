# from django.conf import settings

from rest_framework import serializers, pagination

from .models import Submission, Vote
from musetic.apps.user.serializers import UserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField('get_votes')
    flags = serializers.SerializerMethodField('get_flags')
    comment_count = serializers.SerializerMethodField('get_comment_count')
    uuid = serializers.SerializerMethodField('submission_uuid')

    profile_score = serializers.SerializerMethodField('get_profile_score')
    profile_discussion_score = serializers.SerializerMethodField('get_profile_discussion_score')

    class Meta:
        model = Submission
        fields = ('id', 'uuid', 'submission_type', 'title',
                  'url', 'description', 'user', 'profile_score', 'profile_discussion_score',
                  'thumbnail', 'date_submitted', 'score', 'votes', 'flags',
                  'comment_count')

    user = UserSerializer()

    def get_profile_score(self, obj):
        return obj.get_profile_score()

    def get_profile_discussion_score(self, obj):
        return obj.get_profile_discussion_score()

    def get_votes(self, obj):
        return obj.get_votes()

    def get_flags(self, obj):
        return obj.get_flags()

    def get_comment_count(self, obj):
        return obj.get_comment_count()

    def submission_uuid(self, obj):
        return obj.uuid


class PaginatedSubmissionSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = SubmissionSerializer


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'vote_type', 'submission', 'voter')

    submission = SubmissionSerializer()
    voter = UserSerializer()
