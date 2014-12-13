from ckeditor.widgets import CKEditorWidget
from django.conf import settings


class CustomCKEditorWidget(CKEditorWidget):
    class Media:
        extend = False
        js =( 
            settings.STATIC_URL + 'js/ckeditor/ckeditor.js',
            settings.STATIC_URL + 'js/ckeditor/ckeditor-init.js',
        )
