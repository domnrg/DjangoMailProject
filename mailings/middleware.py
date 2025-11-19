from django.utils.cache import patch_cache_control


class ClientCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # кешируем статику
        if request.path.startswith("/static/"):
            patch_cache_control(response, max_age=86400)  # 1 день

        # кешируем главную страницу
        if request.path == "mailings/":
            patch_cache_control(response, max_age=120)

        return response
