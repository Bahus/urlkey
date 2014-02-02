# -*- coding: utf-8 -*-
from django.conf import settings
from datetime import timedelta

get = lambda s, default: getattr(settings, s, default)

URLKEY_NAME = get('URLKEY_NAME', 'urlkey')
URLKEY_EXPIRATION_TIMEDELTA = get('URLKEY_EXPIRATION_TIMEDELTA', timedelta(days=2))