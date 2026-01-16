import uuid
from django.db import models
from django.utils import timezone

class Career(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    one_line_desc = models.CharField(max_length=500)

    freshers_desc = models.TextField()
    experienced_desc = models.TextField()

    svg_d_value = models.TextField(
        help_text="ONLY SVG path d attribute value"
    )

    last_updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_careers"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "careers"
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title
