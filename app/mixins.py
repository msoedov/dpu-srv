from django.views.decorators.cache import cache_page


class GetCacheMixin:
    """
    This mixin wraps CBS get into cache_page
    """

    cache_timeout = 160

    def get_cache_timeout(self):
        return self.cache_timeout

    def get(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout(), key_prefix="views")(super().get)(
            *args, **kwargs
        )


class PostCacheMixin:
    """
    This mixin wraps CBS get into cache_page
    """

    cache_timeout = 160

    def get_cache_timeout(self):
        return self.cache_timeout

    def post(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout(), key_prefix="views")(super().post)(
            *args, **kwargs
        )


class BrowserCacheControl:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cache-Control"] = "max-age=600"
        return response
