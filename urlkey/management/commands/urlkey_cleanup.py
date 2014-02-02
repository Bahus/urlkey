# -*- coding: utf-8 -*-
from logging import getLogger
from django.core.management.base import BaseCommand

from urlkey.models import URLAction

logger = getLogger('urlkey.cleanup')


class Command(BaseCommand):
    help = "Clean up expired URLActions"

    def handle(self, **options):
        logger.info('URLActions cleanup process started')
        expired_qs = URLAction.get_expired()
        logger.info('Expired actions count: %s', expired_qs.count())
        expired_qs.delete()
        logger.info('URLActions cleanup process ended')