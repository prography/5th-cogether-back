from django.db import models
from django.conf import settings

# Create your models here.
HELP = 'help'
UPDATEREQUEST = 'update'
CREATEREQUEST = 'create'

DATA_SOURCE = [
    (HELP, 'help'),
    (UPDATEREQUEST, 'update'),
    (CREATEREQUEST, 'create'),
]

FREQ = 'freq'
MY = 'my'

DATA_ATTR = [
    (FREQ, 'frequency-questions'),
    (MY, 'my-questions'),
]

WT = 'waiting'
CMP = 'completed'

DATA_STATUS = [
    (WT, 'waiting'),
    (CMP, 'completed'),
]


class HelpCenter(models.Model):
    contents = models.TextField()
    title = models.CharField(max_length=100)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=HELP)
    type = models.CharField(max_length=40, choices=DATA_ATTR, default=MY)
    status = models.CharField(max_length=40, choices=DATA_STATUS, default=WT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    answered_by = models.CharField(max_length=30, blank=True)
    answer = models.TextField(blank=True)


class HelpInfo(models.Model):
    contents = models.TextField()
