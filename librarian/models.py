from django.db import models

from users.models import CustomUser

from .services import today


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Book(TimeStampedModel):
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="books_created",
    )

    def __str__(self):
        return f"{self.title} ({'Available' if self.is_available else 'Not Available'})"


class Lending(TimeStampedModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="lendings"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="lendings")
    start_date = models.DateField(default=today)
    end_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Lending: {self.user.name} -> {self.book.title} (Returned: {self.is_returned})"

    @property
    def total_amount(self):
        days = (self.end_date - self.start_date).days
        days = days if days > 0 else 1
        return days * self.book.price_per_day


class Payment(TimeStampedModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="payments"
    )
    lending = models.OneToOneField(
        Lending, on_delete=models.CASCADE, related_name="payment"
    )
    payment_id = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.payment_id} by {self.user.email} for {self.lending.book.title}"
