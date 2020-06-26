from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)
from .models import BookAuthor, BookPublisher


class BookAuthorAdmin(ModelAdmin):
    model = BookAuthor
    menu_label = 'Author'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required
    #list_display = ('author',)
    #list_filter = ('author',)
    #search_fields = ('author',)


class BookPublisherAdmin(ModelAdmin):
    model = BookPublisher
    menu_label = 'Publisher'  # ditch this to use verbose_name_plural from model
    menu_icon = 'pilcrow'  # change as required


class LibraryGroup(ModelAdminGroup):
    menu_label = 'Catalog'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (BookAuthorAdmin, BookPublisherAdmin)

# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(LibraryGroup)
