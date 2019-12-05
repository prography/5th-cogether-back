import os
from uuid import uuid4
from django.utils import timezone


def uuid_name_upload_to(instance, filename):
    app_label = instance.__class__._meta.app_label
    cls_name = instance.__class__.__name__.lower()
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([
        app_label,
        cls_name,
        ymd_path,
        uuid_name[:2],
        uuid_name + extension,
    ])

def avatar_upload_to(instance, filename):
    app_label = instance.__class__._meta.app_label
    cls_name = instance.__class__.__name__.lower()
    userid_path = str(instance.id)
    file_name = str(instance.id)
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([
        app_label,
        cls_name,
        userid_path,
        file_name+extension,
    ])