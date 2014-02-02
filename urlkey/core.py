# -*- coding: utf-8 -*-
"""
    I said "NO" to Django signals, since they iterate over all registered
    signal, but we already know the actions we want to execute.
"""
import threading
from collections import defaultdict


class ActionsStorage(object):

    def __init__(self):
        self.lock = threading.Lock()
        self.actions = defaultdict(set)

    def add(self, action_type, action_function):
        with self.lock:
            self.actions[action_type].add(action_function)

    def get(self, action_type, default=None):
        return self.actions.get(action_type, default or set())


storage = ActionsStorage()


def get_actions(action_type):
    return storage.get(action_type)


def add_action(action_type, action_function):
    return storage.add(action_type, action_function)
