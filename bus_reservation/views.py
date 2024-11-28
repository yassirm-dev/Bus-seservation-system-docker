from django.http import JsonResponse
from django.core.cache import cache

def request_count_view(request):
    # Retrieve the current request count from the cache, default to 0 if it doesn't exist
    request_count = cache.get('request_count', 0)
    
    # Increment the request count by 1
    request_count += 1
    
    # Save the updated count back to the cache
    cache.set('request_count', request_count, timeout=None)  # 'timeout=None' means it will not expire
    
    # Return the current request count in the response
    return JsonResponse({'request_count': request_count})
