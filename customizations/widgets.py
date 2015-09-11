from ckeditor.widgets import CKEditorWidget
from django.conf import settings
from django.forms.fields import Field


class CustomCKEditorWidget(CKEditorWidget):
    class Media:
        extend = False
        js =(
            settings.STATIC_URL + 'js/ckeditor/ckeditor.js',
            settings.STATIC_URL + 'js/ckeditor/ckeditor-init.js',
        )


# because you can't customize mezzanine form fields attributes
def patched_widget_attrs(self, widget):
    return {'class': 'form-control'}
Field.widget_attrs = patched_widget_attrs
