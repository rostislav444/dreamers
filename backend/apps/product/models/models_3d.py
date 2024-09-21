from django.db import models

from apps.abstract.fields import DeletableFileField, DeletableImageField


class Product3DBlenderModel(models.Model):
    product = models.OneToOneField('product.Product', on_delete=models.CASCADE, related_name='model_3d')
    fov_degrees = models.IntegerField(default=30)
    eye_level = models.DecimalField(default=1.5, max_digits=3, decimal_places=2)
    render_from_eye_level = models.BooleanField(default=False)
    steps = models.IntegerField(default=5)
    obj = DeletableFileField(blank=True, null=True, parent_names_paths=['product'])
    mtl = DeletableFileField(blank=True, null=True, parent_names_paths=['product'])

    class Meta:
        verbose_name = '3D модель'
        verbose_name_plural = '3D модели'

    @property
    def get_name(self):
        return self.product.get_name + '_3d'

    def __str__(self):
        return str(self.id)


class Lights(models.Model):
    model_3d = models.ForeignKey(Product3DBlenderModel, on_delete=models.CASCADE, related_name='lights')
    power = models.IntegerField(default=1000)
    pos_x = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    pos_y = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    pos_z = models.DecimalField(default=0, max_digits=20, decimal_places=4)


class Camera(models.Model):
    model_3d = models.ForeignKey(Product3DBlenderModel, on_delete=models.CASCADE, related_name='cameras')
    pos_x = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    pos_y = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    pos_z = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    rad_x = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    rad_y = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)
    rad_z = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True)

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        ordering = ['-rad_z']

class CameraInteriorLayer(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='interior_layers')
    interior_layer = models.ForeignKey('interior.InteriorLayer', on_delete=models.CASCADE, related_name='cameras')

    def __str__(self):
        return str(self.interior_layer)


class CameraInteriorLayerMaterialGroup(models.Model):
    layer = models.ForeignKey(CameraInteriorLayer, on_delete=models.CASCADE, related_name='material_groups')
    material_group = models.ForeignKey('interior.InteriorLayerMaterialGroup', on_delete=models.CASCADE, related_name='cameras')

    def __str__(self):
        return str(self.material_group)


class CameraInteriorLayerMaterial(models.Model):
    group = models.ForeignKey(CameraInteriorLayerMaterialGroup, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey('interior.InteriorMaterial', on_delete=models.CASCADE, related_name='material_scene')

    def __str__(self):
        return str(self.material)


class CameraInteriorLayerMaterialImage(models.Model):
    scene_material = models.OneToOneField(CameraInteriorLayerMaterial, on_delete=models.CASCADE, related_name='image')
    image = DeletableImageField(parent_names_paths=['scene_material.group.layer'])
    image_thumbnails = models.JSONField(default=dict, blank=True, null=True)