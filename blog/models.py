from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet

from wagtail.api import APIField


class BlogIndexPage(Page):
    intro = models.CharField(max_length=250)
    menu_weight = models.PositiveSmallIntegerField(default=99)

    promote_panels = Page.promote_panels + [
        FieldPanel('menu_weight', classname="full")
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = BlogPage.objects.in_site(request.site).live().order_by('-first_published_at')
        #blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        context['firstpage'] = blogpages.first()
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
    )
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(features=['code','blockquote','bold','hr','italic',
            'h2','h3','h6','ol','ul','link'])),
        ('image', ImageChooserBlock()),
        ('code', blocks.TextBlock()),
        ])
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Blog Information"),
        FieldPanel('intro'),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
    ]
    
    api_fields = [
		APIField('date'),
		APIField('intro'),
		APIField('image'),
		APIField('body'),
		APIField('tags'),
    ]




class BlogTagIndexPage(Page):
    menu_weight = models.PositiveSmallIntegerField(default=99)

    promote_panels = Page.promote_panels + [
        FieldPanel('menu_weight', classname="full")
    ]

    def get_context(self, request):

        # Filter by tag
        if request.GET.get('tag'):
            tag = request.GET.get('tag')
            blogpages = BlogPage.objects.in_site(request.site).live().filter(tags__name=tag).order_by('-first_published_at')
        else:
            blogpages = BlogPage.objects.in_site(request.site).live().order_by('-first_published_at')
        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context
