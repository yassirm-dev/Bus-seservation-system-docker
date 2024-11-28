# myapp/middleware.py

import logging

# Set up a simple logger
logger = logging.getLogger(__name__)

class RequestCountMiddleware:
    # Initialize request count
    request_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Increment the request count for each request
        RequestCountMiddleware.request_count += 1

        # You can log the request count to a file or console for monitoring
        logger.info(f"Total requests sent to the app: {RequestCountMiddleware.request_count}")

        # Process the request
        response = self.get_response(request)
        return response
