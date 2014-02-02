# -*- coding: utf-8 -*-
from urlkey.models import URLAction


class URLKeyActionMiddleware(object):
    """
        Receive actions from request and execute them.
    """

    def process_request(self, request):
        action = URLAction.get_from_request(request)
        if action:
            action.execute(request=request)