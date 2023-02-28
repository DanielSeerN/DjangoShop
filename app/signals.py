from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Product


@receiver(pre_delete, sender=Product)
def delete_image(sender, instance, **kwargs):
    if instance.image.path:
        instance.image.delete(False)
