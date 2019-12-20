from django.shortcuts import render
from rest_framework import viewsets, mixins
from django.contrib.auth.mixins import LoginRequiredMixin

from help.serializers import HelpCenterSerializer, HelpInfoSerializer
from help.models import HelpCenter, FREQ, HelpInfo


# Create your views here.
class MyHelpCenterViewSet(viewsets.ModelViewSet): # LoginRequiredMixin,
    serializer_class = HelpCenterSerializer

    def get_queryset(self):
        return HelpCenter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FreqHelpCenterViewSet(viewsets.ModelViewSet):
    serializer_class = HelpCenterSerializer
    queryset = HelpCenter.objects.filter(type=FREQ)


class HelpInfoViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    serializer_class = HelpInfoSerializer
    queryset = HelpInfo.objects.all().order_by('id')
