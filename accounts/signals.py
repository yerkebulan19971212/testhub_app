from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from accounts.models import User
from quizzes.models import Variant, UserVariant


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        main_variants = Variant.objects.filter(main=True).order_by('variant')
        user_variants = [UserVariant(
            user=instance,
            variant=v,

        ) for v in main_variants]
        UserVariant.objects.bulk_create(user_variants)
