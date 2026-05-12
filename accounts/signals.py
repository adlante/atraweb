from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="create_unique_profile_for_user")
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    این سیگنال بلافاصله بعد از ساخته شدن یک یوزر جدید،
    یک پروفایل خام و خالی رو به صورت اتوماتیک براش می‌سازه.
    """
    if created:
        # 💥 تغییر طلایی: استفاده از get_or_create به جای create
        Profile.objects.get_or_create(user=instance)
    else:
        # در صورت آپدیت شدن یوزر، پروفایلش هم آپدیت میشه
        if hasattr(instance, 'profile'):
            instance.profile.save()
