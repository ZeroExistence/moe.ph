from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks
from wagtail.snippets.models import register_snippet

from wagtail.core.models import Page


class HomePage(Page):
    pass

class FlatPage(Page):
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(features=['code','blockquote','bold','hr','italic',
            'h2','h3','h6','ol','ul','link'])),
        ('image', ImageChooserBlock()),
        ('code', blocks.TextBlock()),
        ])
    menu_weight = models.PositiveSmallIntegerField(default=99)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body', classname="full"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('menu_weight', classname="full")
    ]

@register_snippet
class ExternalLink(models.Model):
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)
    weight = models.PositiveSmallIntegerField(default=99)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
        FieldPanel('weight'),
    ]

    def __str__(self):
        return self.text
