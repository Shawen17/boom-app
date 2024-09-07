from django.utils.deprecation import MiddlewareMixin
from lendsqr.utility import push_metrics_to_redis  # Import your function


class MetricsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        push_metrics_to_redis()
        return response
