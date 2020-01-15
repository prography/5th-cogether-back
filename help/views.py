from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework import permissions

from help.serializers import HelpCenterSerializer, HelpInfoSerializer
from help.models import HelpCenter, FREQ, HelpInfo


# Create your views here.
class MyHelpCenterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HelpCenterSerializer

    def get_queryset(self):
        return HelpCenter.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        request_data = self.request.data['user']
        my_user = get_user_model().objects.get(pk=request_data)
        serializer.save(user=my_user)


class FreqHelpCenterViewSet(viewsets.ModelViewSet):
    serializer_class = HelpCenterSerializer
    queryset = HelpCenter.objects.filter(type=FREQ)


class HelpInfoViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    serializer_class = HelpInfoSerializer
    queryset = HelpInfo.objects.all().order_by('id')
