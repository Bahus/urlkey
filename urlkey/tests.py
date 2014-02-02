# -*- coding: utf-8 -*-
import json
from datetime import timedelta
from httplib import OK
from django.conf import settings
from django.conf.urls import url, patterns
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth.models import User

from urlkey.models import URLAction
from urlkey.settings import URLKEY_NAME, URLKEY_EXPIRATION_TIMEDELTA
from urlkey.decorators import register_urlaction

from tools.testing import reload_from_db

from django_dynamic_fixture import G


class URLKeyTest(TestCase):
    urls = 'urlkey.tests'

    test_data = {
        'email': 'bahus@test.com',
        'password': 'Qwerty',
        'is_staff': False,
    }

    def setUp(self):
        self._old_middlewares = settings.MIDDLEWARE_CLASSES
        settings.MIDDLEWARE_CLASSES += ('urlkey.middleware.URLKeyActionMiddleware', )

        self.user = G(User, **self.test_data)

    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self._old_middlewares

    def test_user_custom_action(self):
        action_type = 'set_is_staff'

        url_action = URLAction.create(action_type, {'user_id': self.user.id})

        @register_urlaction(action_type)
        def action_set_stuff(action, **kwargs):
            user_id = action.data.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            user.is_staff = True
            user.save()
            self.assertIn('test', kwargs)

        self.assertFalse(self.user.is_staff)
        url_action.execute(test=True)
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.is_staff)

    def test_urlaction_object(self):
        action_type = 'test_type'
        data = {'test': True, 'welcome': 123}

        action = URLAction.create(action_type, data)
        self._action_executed = False

        @register_urlaction(action_type)
        def simple(action, **kwargs):
            self.assertEqual(action.action_type, action_type)
            self.assertDictEqual(action.data, data)

            m = timedelta(minutes=1)
            n = now() + URLKEY_EXPIRATION_TIMEDELTA

            self.assertTrue((n - m) < action.expired < (n + m))
            self.assertIn('request', kwargs)
            self._action_executed = True

        test_url = '/urlkey_test_view/'
        self.assertEqual(
            action.wrap_url(test_url),
            test_url + '?' + URLKEY_NAME + '=' + action.id
        )

        response = self.client.get(test_url)
        self.assertEqual(response.status_code, OK)
        self.assertFalse(self._action_executed)

        response = self.client.get(action.wrap_url(test_url))
        self.assertEqual(response.status_code, OK)
        self.assertTrue(self._action_executed)
        del self._action_executed


def my_view(request):
    return HttpResponse('test')


urlpatterns = patterns('',
    url('urlkey_test_view/', my_view, name='urlkey_test_view'),
)



