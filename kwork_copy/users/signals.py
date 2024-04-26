from django.contrib.auth import get_user_model, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import FreelancerProfile, CustomerProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler for creating or updating a user Profile when a User instance
    is saved.

    Args:
        sender (Object): The sender of the signal.
        instance (User): The User instance that was saved.
        created (bool): A flag indicating if the instance was just created.
        **kwargs: Additional keyword arguments passed to the signal handler.
    """
    if created and not hasattr(instance, '_creating_from_admin'):
        if instance.is_freelancer:
            FreelancerProfile.objects.create(user=instance)
        else:
            CustomerProfile.objects.create(user=instance)
        instance.profile.save()
