from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property

logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics
    """
    try:
        # Connect to Redis via django_redis
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO stats
        info = redis_conn.info()
        
        # Extract keyspace hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 4),
            'hit_ratio_percentage': round(hit_ratio * 100, 2)
        }
        
        # Log metrics
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
            'hit_ratio_percentage': 0
        }