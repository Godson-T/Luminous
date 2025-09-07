from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICE = (
        (LIVE, 'Live'),
        (DELETE, 'Delete')
    )

    name = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)   # made optional for auto create
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=10, blank=True, null=True)  # made optional for auto create
    delete_status = models.IntegerField(choices=DELETE_CHOICE, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username


# Signal to create or update Customer automatically
@receiver(post_save, sender=User)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        # Create a customer profile with safe defaults
        Customer.objects.create(user=instance, name=instance.username)
    else:
        # Update existing profile if it exists
        if hasattr(instance, 'customer_profile'):
            instance.customer_profile.save()
