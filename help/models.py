from django.db import models
from django.conf import settings
from cogether.storages import MediaStorage
from cogether.utils import help_image_upload_to

# Create your models here.
HELP = 'help'
UPDATEREQUEST = 'update'
CREATEREQUEST = 'create'

DATA_TYPE = [
    (HELP, '1:1 요청'),
    (UPDATEREQUEST, '수정 요청'),
    (CREATEREQUEST, '게시 요청'),
]

WAITING = 'waiting'
COMPLETED = 'completed'

DATA_STATUS = [
    (WAITING, '답변 대기중'),
    (COMPLETED, '답변 완료'),
]


class Answer(models.Model):
    answer = models.TextField(blank=True)


class Question(models.Model):
    contents = models.TextField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=DATA_TYPE, default=HELP)
    status = models.CharField(max_length=40, choices=DATA_STATUS, default=WAITING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.title


class HelpContentImage(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(
        storage=MediaStorage(),
        upload_to=help_image_upload_to
    )
