from .serializers import SubmissionSerializer, VoteSerializer
from .models import Vote, Submission

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


class SubmissionAPIList(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAdminUser,)


class SubmissionAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAdminUser,)


class VoteAPIList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAdminUser,)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'vote': reverse('vote-list', request=request, format=format),
        'submission': reverse('submission-list', request=request, format=format),
    })
