from django.db import models
from apps.abstract.fields import DeletableImageField


class Product3dModelSceneMaterial(models.Model):
    camera = models.ForeignKey('product.CameraLocations', on_delete=models.CASCADE)
    material = models.ForeignKey('material.ProductPartMaterials', on_delete=models.CASCADE)
    image = DeletableImageField()
