from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google
from django.core.validators import FileExtensionValidator
from django.db import models
from PIL import Image

THEME = (
    # In-system value - Show value
    ('', 'Dark Mode (Default)'),
    ('light', 'Light Mode'),
    # ('sync', 'Sync With System Settings')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    cover = models.ImageField(default='default_cover.png', upload_to='cover_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    about_me = models.TextField(default='Hello there!', max_length=120, blank=True)
    osu_username = models.CharField(default='', max_length=50, blank=True)
    oauth_first_migrate = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass
        # Use pillow to resize profile image and cover image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
        cover = Image.open(self.cover.path)
        if cover.height > 1080 or cover.width > 1920:
            cover.thumbnail((1920, 1080))
            cover.save(self.cover.path)


class Config(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    update_profile_every_login = models.BooleanField(default=False)
    theme = models.TextField(choices=THEME, default='')

    def __str__(self):
        return f'{self.user.username} Config'
