from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponse


def role_required():
    def decorator(view_func):          # restrict normal users from gaining access to admin panel
        @login_required()
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_admin:
                return HttpResponse("URL NOT FOUND.")
            return view_func(request, *args, **kwargs)
        return wrapper

    return decorator