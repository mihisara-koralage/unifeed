from django.db import models
from django.conf import settings

class Listing(models.Model):

    class Category(models.TextChoices):
        BOOKS       = 'books',       'Books & Notes'
        ELECTRONICS = 'electronics', 'Electronics'
        CLOTHING    = 'clothing',    'Clothing'
        FURNITURE   = 'furniture',   'Furniture'
        SPORTS      = 'sports',      'Sports & Fitness'
        OTHER       = 'other',       'Other'

    class Condition(models.TextChoices):
        NEW         = 'new',         'New'
        LIKE_NEW    = 'like_new',    'Like New'
        GOOD        = 'good',        'Good'
        FAIR        = 'fair',        'Fair'

    seller      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title       = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    category    = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    condition   = models.CharField(max_length=10, choices=Condition.choices, default=Condition.GOOD)
    location    = models.CharField(max_length=200, help_text='Where to meet on campus')
    contact_info = models.CharField(max_length=200, help_text='Phone, WhatsApp, or email')
    is_active   = models.BooleanField(default=True)   # seller can mark as sold
    is_approved = models.BooleanField(default=True)   # admin can remove bad listings
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} — LKR {self.price}'

    @property
    def primary_image(self):
        return self.images.first()


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='marketplace_images/')
    order   = models.PositiveSmallIntegerField(default=0)  # 0=first, 1=second, 2=third

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Image {self.order} for {self.listing.title}'


class Report(models.Model):

    class Reason(models.TextChoices):
        SCAM        = 'scam',       'Scam or fraud'
        PROHIBITED  = 'prohibited', 'Prohibited item'
        MISLEADING  = 'misleading', 'Misleading description'
        OTHER       = 'other',      'Other'

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    listing  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reports')
    reason   = models.CharField(max_length=20, choices=Reason.choices)
    details  = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reporter', 'listing')  # one report per user per listing

    def __str__(self):
        return f'Report on "{self.listing.title}" by {self.reporter.email}'