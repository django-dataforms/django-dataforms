from django.http import Http404
from django.shortcuts import render
from app_settings import FIELD_MAPPINGS, REMOTE_JQUERY_JS, REMOTE_JQUERY_CSS

def build(request):
    
    fields = FIELD_MAPPINGS
    context = {
        'fields' : fields,
        'media_js' : REMOTE_JQUERY_JS,
        'media_css' : REMOTE_JQUERY_CSS
    }
    
    return render(request, 'dataforms/build.html', context)


def get_field(request, field):
    
    field_str = field
    field = FIELD_MAPPINGS.get(field, None)
    
    if not field:
        raise Http404
    
    # Replace the string arguments with the actual modules or classes
    for key in ('class', 'widget'):
        if not field.has_key(key):
            continue
        
        value = field[key]
        if isinstance(value, str) or isinstance(value, unicode):
            name = value.split(".")
            module_name = ".".join(name[:-1])
            class_name = name[-1]
            module = __import__(module_name, fromlist=[class_name])
            # Replace the string with a class pointer
            field[key] = getattr(module, class_name)
    
    field_kwargs={}
    if field.has_key('widget'):
        field_kwargs['widget'] = field['widget']()
    
    final_field = field['class'](**field_kwargs)
    rendered_field = final_field.widget.render(field_str, '')
               
    context = {
        'title' : field_str,
        'field' : rendered_field,
    }
    
    return render(request, 'dataforms/get_field.html', context)
    