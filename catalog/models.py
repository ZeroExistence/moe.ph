from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey

# Create your models here.


class BookPublisher(models.Model):
    publisher = models.CharField(max_length=100)
    panels = [ FieldPanel('publisher') ]

    def __str__(self):
        return self.publisher


class BookAuthor(models.Model):
    author = models.CharField(max_length=100)
    panels = [ FieldPanel('author') ]

    def __str__(self):
        return self.author


class CatalogIndexPage(Page):
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
        catalogpages = CatalogPage.objects.in_site(request.site).live().order_by('title')
        context['catalogpages'] = catalogpages
        return context


class CatalogPage(Page):
    publisher = models.ForeignKey(BookPublisher, null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(BookAuthor, null=True, blank=True, on_delete=models.SET_NULL)
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('author'),
            FieldPanel('publisher'),
        ], heading="Catalog Information"),
        InlinePanel('catalog_gallery_images', label="Gallery images"),
    ]


class CatalogPageGalleryImage(Orderable):
    page = ParentalKey(CatalogPage, on_delete=models.CASCADE, related_name='catalog_gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [ ImageChooserPanel('image') ]


class CatalogListPage(Page):
    menu_weight = models.PositiveSmallIntegerField(default=99)

    promote_panels = Page.promote_panels + [
        FieldPanel('menu_weight', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        catalogpages = CatalogPage.objects.in_site(request.site).live().order_by('title')
        context['catalogpages'] = catalogpages
        return context
