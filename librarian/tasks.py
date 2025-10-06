from datetime import date

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from librarian.models import Lending

from .models import Payment


@shared_task
def send_payment_completed_email(instance_id):
    try:
        payment = Payment.objects.select_related(
            "lending__book__created_by", "user"
        ).get(id=instance_id)
        book_admin = payment.lending.book.created_by
        if book_admin and book_admin.email:
            send_mail(
                subject="Book Purchased",
                message=(
                    f"Your book '{payment.lending.book.title}' has been purchased by {payment.user.name}.\n"
                    f"Return date: {payment.lending.end_date.strftime('%Y-%m-%d')}\n"
                    f"Amount: {payment.amount}\n"
                    f"Payment ID: {payment.payment_id}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[book_admin.email],
            )
    except Exception as e:
        print(e)


@shared_task
def send_book_due_reminder():
    today = date.today()
    lendings = Lending.objects.filter(end_date=today, is_returned=False)
    for lending in lendings:
        if lending.user.email:
            send_mail(
                subject="Book Due Reminder",
                message=(
                    f"Hi {lending.user.name},\n"
                    f"Your book '{lending.book.title}' is due today ({lending.end_date}). "
                    f"Please return it on time."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[lending.user.email],
            )


@shared_task
def set_payment_complete_task(instance_id):
    try:
        payment = Payment.objects.get(id=instance_id)
        payment.status = Payment.PaymentStatus.COMPLETED
        payment.save()
    except Payment.DoesNotExist:
        pass
