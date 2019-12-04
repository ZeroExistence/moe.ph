from django.db import models

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel

from django.contrib.contenttypes.models import ContentType

# Create your models here.

class KinkPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'KinkPage',
        related_name='kink_tag',
        on_delete=models.CASCADE
    )


class KinkIndexPage(Page):
    intro = models.CharField(max_length=250)
    menu_weight = models.PositiveSmallIntegerField(default=99)

    promote_panels = Page.promote_panels + [
        FieldPanel('menu_weight', classname="full")
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        kinkpages = KinkPage.objects.in_site(request.site).live().order_by('-first_published_at')
        context['kinkpages'] = kinkpages
        return context


class KinkPage(Page):
    date = models.DateField("Post Date")
    tags = ClusterTaggableManager(through=KinkPageTag, blank=True)
    author = models.CharField(max_length=100)
    source = models.URLField()
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading="Page Information"),
        MultiFieldPanel([
            FieldPanel('author'),
            FieldPanel('source'),
        ], heading="Work Information"),
        InlinePanel('kink_gallery_images', label="Gallery images"),
    ]


class KinkPageGalleryImage(Orderable):
    page = ParentalKey(KinkPage, on_delete=models.CASCADE, related_name='kink_gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]


class KinkTagIndexPage(Page):
    menu_weight = models.PositiveSmallIntegerField(default=99)

    promote_panels = Page.promote_panels + [
        FieldPanel('menu_weight', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Filter by tag
        if request.GET.get('tag'):
            tag = request.GET.get('tag')
            context['kinkpages'] = KinkPage.objects.in_site(request.site).live().filter(tags__name=tag).order_by('-first_published_at')
        else:
            #context['kinktags'] = Tag.objects.all().distinct('taggit_taggeditem_items__tag')
            context['kinktags'] = KinkPageTag.objects.all()
        return context
