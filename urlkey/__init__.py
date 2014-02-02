# -*- coding: utf-8 -*-
"""
    This applications is intended retrieve unique identificator from
    URI and perform any related actions.

    Примеры использования:

    1) Добавьте в настройки джанго в опцию MIDDLEWARE_CLASSES:
    "urlkey.middleware.URLKeyActionMiddleware"

    2) Создайте новое "действие", например необходимо сбросить пароль
    пользователю на рандомный:

    from urlkey.models import URLAction

    def get_reset_password_url(user):
        action = URLAction.create(
            'reset_password',
            {'user_id': user.pk},
            expired=now() + timedelta(days=1),
        )
        return action.wrap_url(reverse('user_reset_password'))

    3) Создайте обработчик действия:

    from django.shortcuts import get_object_or_404
    from urlkey.decorators import register_urlaction

    @register_urlaction('reset_password')
    def reset_users_password(action, request, **kwargs):
        user = get_object_or_404(User, pk=action.data.get('user_id'))
        user.set_password(random_password)
        user.save()

    4) Пошлите пользователю ссылку из get_reset_password_url() и как только
    он по ней перейдет - его пароль изменится.
"""
