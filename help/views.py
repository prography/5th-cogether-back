from rest_framework import viewsets
from rest_framework import permissions

from help.serializers import QuestionSerializer, ImageSerializer
from help.models import Question


# Create your views here.
class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HelpImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save()
