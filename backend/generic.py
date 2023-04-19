from django.db.models import Model


class Base(Model):
    def __iter__(self):
        for field_name in self._meta.fields():
            try:
                value = getattr(self, field_name)
            except:
                value = None
            yield (field_name, value)

    def __getItem__(self, fieldname):
        try:
            return getattr(self, fieldname)
        except:
            return None

    def __setItem__(self, fieldname, value):
        try:
            return setattr(self, fieldname, value)
        except:
            return None

    class Meta:
        abstract = True
