# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.db.utils import IntegrityError
from django.utils import timezone

from django_extensions.db.fields.json import JSONField
from urlobject import URLObject

from urlkey import settings
from urlkey.core import get_actions


class URLAction(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    action_type = models.CharField(max_length=32)
    expired = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    onetime = models.BooleanField(default=True)
    data = JSONField()

    class Meta:
        verbose_name = 'URL Action'
        verbose_name_plural = 'URL Actions'
        ordering = ['-created']

    def __unicode__(self):
        return u'<URL Action %s expired at %s>' % (self.action_type, self.expired)

    def execute(self, **kwargs):
        for action_function in get_actions(self.action_type):
            action_function(action=self, **kwargs)

        if self.onetime:
            self.delete()

    def wrap_url(self, url):
        o_url = URLObject(url)
        return o_url.add_query_param(settings.URLKEY_NAME, self.id)

    @classmethod
    def get_from_request(cls, request):
        action_id = request.REQUEST.get(settings.URLKEY_NAME)

        if not action_id:
            return None

        try:
            return cls.objects.get(id=action_id)
        except (cls.DoesNotExist, TypeError, ValueError):
            pass

        return None

    @classmethod
    def create(cls, action_type, data, expired=None, **kwargs):
        expired = (
            expired or (timezone.now() + settings.URLKEY_EXPIRATION_TIMEDELTA)
        )

        return cls.objects.create(
            id=cls.generate_action_id(),
            action_type=action_type,
            expired=expired,
            data=data,
            **kwargs
        )

    @classmethod
    def get_expired(cls):
        return cls.objects.filter(expired__lte=timezone.now())

    @staticmethod
    def generate_action_id():
        return uuid.uuid4().hex




