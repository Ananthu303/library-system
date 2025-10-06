import uuid

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import UserDetailSerializer

from .models import Book, Lending, Payment


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ("created_at", "updated_at")
        read_only_fields = ("created_by",)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["is_available"] = True
        return super().create(validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("status", "user", "lending", "payment_id")


class LendingSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.filter(is_available=True), write_only=True, source="book"
    )
    book = BookSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Lending
        exclude = ("created_at", "updated_at")
        read_only_fields = ("payment",)

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            with transaction.atomic():
                lending = Lending.objects.create(user=user, **validated_data)
                test_payment_id = str(uuid.uuid4()).replace("-", "").upper()[:12]
                Payment.objects.create(
                    user=user,
                    lending=lending,
                    amount=lending.total_amount,
                    payment_id=test_payment_id,
                )
            return lending

        except Exception as e:
            raise ValidationError(
                {"detail": f"Failed to create lending/payment: {str(e)}"}
            )
