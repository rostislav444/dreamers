from rest_framework import viewsets, mixins, generics
from django.db.models import Prefetch, Q
from apps.product.models import ProductClass, ProductAttribute, Sku, ProductClassOption, ProductClassOptionGroup
from apps.catalogue.serializers import CatalogueProductClassSerializer


class CatalogueProductViewSet(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin, viewsets.ViewSet):
    serializer_class = CatalogueProductClassSerializer

    def get_queryset(self):
        options_q = Q()
        sku_q = Q()

        for k, v in self.request.GET.items():
            group = k.replace('clr-', '')
            ids = v.split(',')
            options_q |= Q(
                Q(attribute_group__slug=group) &
                ~Q(value_attribute__color__id__in=ids)
            )
            sku_q |= Q(
                Q(options__option__attribute_group__attribute_group__slug=group) &
                ~Q(options__option__value_attribute__color__id__in=ids)
            )


        return ProductClass.objects.all().prefetch_related(
            Prefetch('option_groups', queryset=ProductClassOptionGroup.objects.filter(image_dependency=True)),
            Prefetch('option_groups__options', queryset=ProductClassOption.objects.exclude(options_q)),
            Prefetch('products__sku', queryset=Sku.objects.exclude(sku_q)),
        )

    # def get_queryset(self):
    #     # pk_list = [10, 2, 1]
    #     # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
    #     # queryset = MyModel.objects.filter(pk__in=pk_list).order_by(preserved)
    #
    #     param = self.request.GET.get('clr-tsvet-korpusa', '').split(',')
    #
    #
    #     #TODO Rebuild with ProductClass
    #     return Product.objects.all().prefetch_related(
    #         Prefetch('sku', queryset=Sku.objects.filter(
    #             Q(options__option__value_attribute__color__id__in=[267])
    #         )),
    #         # Prefetch('product_class__option_group__options', queryset=ProductClassOption.objects.filter(
    #         #     Q(value_attribute__color__id__in=[267])
    #         # )),
    #
    #     )
