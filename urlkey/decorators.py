# -*- coding: utf-8 -*-
from functools import wraps
from urlkey.core import add_action


def register_urlaction(action_type):

    def _decorator(func):
        # add action
        add_action(action_type, func)

        @wraps(func)
        def _wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return _wrapper

    return _decorator