from django.db import models
from slugify import slugify


class NameSlug(models.Model):
    name = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=1024, blank=True, null=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_name

    @property
    def get_name(self):
        return self.name

    def get_slug(self):
        name = self.get_name
        if name:
            return slugify(self.get_name)
        return None

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(NameSlug, self).save(*args, **kwargs)

