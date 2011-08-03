from django.core.cache import cache as cache_backend

def cache_set_with_tags(key, value, tags=[], timeout=None):
    for tag in tags:
        tag_list = cache_backend.get(tag)
        if tag_list:
            tag_list.append(key)
        else:
            tag_list = [key]
        cache_backend.set(tag, tag_list, timeout)
    cache_backend.set(key, value, timeout)
    
def cache_delete_by_tags(tags=[]):
    for tag in tags:
        tag_list = cache_backend.get(tag)
        if tag_list:
            for key in tag_list:
                cache_backend.delete(key)
        cache_backend.delete(tag)
        
cache_backend.set_with_tags = cache_set_with_tags
cache_backend.cache_delete_by_tags = cache_delete_by_tags
cache = cache_backend