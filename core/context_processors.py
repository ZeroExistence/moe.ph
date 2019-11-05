from wagtail.core.models import Page
from home.models import FlatPage

def site_menu(request):
    if Page.objects.in_site(request.site).live().in_menu():
        site_menu = Page.objects.in_site(request.site).live().in_menu()
    else:
        site_menu = Page.objects.none()

    return {'site_menu': site_menu}

def flat_page_menu(request):
    if FlatPage.objects.live().in_menu():
        flat_page_menu = FlatPage.objects.live().in_menu()
    else:
        flat_page_menu = FlatPage.objects.none()

    return {'flat_page_menu': flat_page_menu}
