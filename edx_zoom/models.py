from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from opaque_keys.edx.django.models import CourseKeyField, UsageKeyField
from opaque_keys.edx.keys import UsageKey


@python_2_unicode_compatible
class LTICredential(models.Model):
    course_id = CourseKeyField(max_length=255, unique=True)
    key = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    launch_url = models.URLField(max_length=1024, default='https://applications.zoom.us/lti/rich', blank=True)

    def __str__(self):
        return 'LTI credential for %s' % self.course_id


@python_2_unicode_compatible
class LaunchLog(models.Model):
    """
    Records first/last user access to each Zoom XBlocks
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    course_id = CourseKeyField(max_length=255, db_index=True)
    location = UsageKeyField(max_length=255)
    managed = models.BooleanField(db_index=True, default=False)
    first_access = models.DateTimeField(auto_now_add=True, db_index=True)
    last_access = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        unique_together = ('user', 'location')

    @classmethod
    def update(cls, user_id, usage_key, managed):
        obj, created = cls.objects.get_or_create(
            user_id=user_id,
            location=usage_key,
            course_id=usage_key.course_key, defaults={'managed': managed})
        if not created:
            obj.last_access = now()
            obj.managed = managed
            obj.save()
        return obj

    def __str__(self):
        return f"{self.user_id} visited {self.location} on {self.last_access}"
