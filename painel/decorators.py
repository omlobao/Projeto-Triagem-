from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Decorator that restricts access to superusers and staff users."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Acesso negado. Você não tem permissão para acessar o painel administrativo.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped


class AdminRequiredMixin:
    """Mixin for class-based views that restricts access to admin users."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Acesso negado. Você não tem permissão para acessar o painel administrativo.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
