from __future__ import absolute_import, unicode_literals

from django.db import models
from opaque_keys.edx.django.models import CourseKeyField


class LTICredential(models.Model):
    course_id = CourseKeyField(max_length=255, unique=True)
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    launch_url = models.URLField(max_length=1024, default='https://applications.zoom.us/lti/rich', blank=True)

    def __str__(self):
        return 'LTI credential for %s' % self.course_id
