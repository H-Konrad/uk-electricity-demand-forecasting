import requests_cache
from retry_requests import retry

def elexon_session():
    cache_session = requests_cache.CachedSession(
        cache_name = '.elexon_cache', 
        expire_after = 3600
    )
    retry_session = retry(
        cache_session, 
        retries = 5, 
        backoff_factor = 0.2
    )

    return retry_session

def weather_data_session():
    cache_session = requests_cache.CachedSession(
        cache_name = '.weather_cache', 
        expire_after = 3600
    )
    retry_session = retry(
        cache_session, 
        retries = 5, 
        backoff_factor = 0.2
    )

    return retry_session