from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class URL(models.Model):
    long_url = models.URLField(
        max_length=2048,
        help_text="The original URL to be shortened"
    )
    short_url = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text="The shortened URL identifier"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the URL was created"
    )
    last_accessed = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the URL was last accessed"
    )
    access_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times the URL has been accessed"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the shortened URL is active"
    )

    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_url} -> {self.long_url}"

    def clean(self):
        # Validate the long URL format
        validator = URLValidator()
        try:
            validator(self.long_url)
        except ValidationError:
            raise ValidationError({"long_url": "Enter a valid URL."})

    def increment_access_count(self):
        """Increment the access count for this URL"""
        self.access_count += 1
        self.save(update_fields=["access_count", "last_accessed"])
