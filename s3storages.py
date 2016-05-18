# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

MediaRootS3BotoStorage = lambda: S3BotoStorage(bucket=settings.AWS_MEDIA_BUCKET_NAME)
StaticRootS3BotoStorage = lambda: S3BotoStorage(bucket=settings.AWS_STORAGE_BUCKET_NAME)
