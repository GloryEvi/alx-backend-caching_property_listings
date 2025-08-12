from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Get all properties with Redis caching for 1 hour using Django's low-level cache API
    """
    # Check Redis for cached data
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        return cached_properties
    
    # If not found in cache, fetch from database
    queryset = Property.objects.all()
    
    # Store in Redis cache for 1 hour (3600 seconds)
    cache.set('all_properties', queryset, 3600)
    
    return queryset