from celery import shared_task

from apps.product.utils import generate_product_class_sku, generate_product_sku


@shared_task
def task_generate_product_class_sku(pk):
    generate_product_class_sku(pk)


@shared_task
def task_generate_product_sku(pk):
    generate_product_sku(pk)
