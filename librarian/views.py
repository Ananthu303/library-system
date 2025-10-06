from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser

from .models import Book, Lending, Payment
from .permissions import CanManageBooks
from .serializers import BookSerializer, LendingSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, CanManageBooks]


class LendingViewSet(viewsets.ModelViewSet):
    serializer_class = LendingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == CustomUser.UserType.USER:
            return Lending.objects.filter(
                user=user, payment__status=Payment.PaymentStatus.COMPLETED
            ).select_related("book", "payment")
        return Lending.objects.all()
