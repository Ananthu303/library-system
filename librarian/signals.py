from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment


from .tasks import send_payment_completed_email, set_payment_complete_task


@receiver(post_save, sender=Payment)
def notify_admin_on_purchase(sender, instance, created, **kwargs):
    if created:
        # set payment status completed for testing purpose
        set_payment_complete_task.apply_async((instance.id,), countdown=10)

    # Notify book creator
    if instance.status == Payment.PaymentStatus.COMPLETED:
        book_admin = instance.lending.book.created_by
        if book_admin and book_admin.email:
            send_payment_completed_email.delay(instance.id)
