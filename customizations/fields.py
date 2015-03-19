from django.core.files.storage import default_storage
from django.db import models
from django.utils.six import with_metaclass
from mezzanine.core.fields import FileField

base_classes = (models.ImageField,)

if not issubclass(models.ImageField, FileField):
    base_classes = (FileField,) + base_classes


class FileBrowseImageField(with_metaclass(models.SubfieldBase, FileField)):

    class ProxyFile(object):
        def __init__(self, target_field):
            self.target_field = target_field

        def __get__(self, instance=None, owner=None):
            name = instance.__dict__[self.target_field.name].name
            return models.fields.files.FieldFile(
                instance, self.target_field, name)

    def __init__(self, file_obj_name='image_file', *args, **kwargs):
        self.storage = kwargs.pop('storage', None) or default_storage
        super(FileBrowseImageField, self).__init__(*args, **kwargs)
        self.file_obj_name = file_obj_name

    def contribute_to_class(self, cls, name):
        super(FileBrowseImageField, self).contribute_to_class(cls, name)
        setattr(cls, self.file_obj_name, self.ProxyFile(self))