from django import template
from home.models import ExternalLink

register = template.Library()


# Advert snippets
@register.inclusion_tag('home/external_links.html', takes_context=True)
def external_links(context):
    return {
        'external_links': ExternalLink.objects.all().order_by('weight'),
        'request': context['request'],
    }
