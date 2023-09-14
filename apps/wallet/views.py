from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework_json_api import filters as jsonapi_filters
from rest_framework_json_api import views

from apps.wallet.models import Transaction, Wallet
from apps.wallet.serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(views.ModelViewSet):
    """
    ViewSet для работы с моделью Wallet.

    Позволяет создавать, просматривать, обновлять и удалять кошельки.

    Поддерживает фильтрацию, сортировку и пагинацию.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = PageNumberPagination
    filter_backends = (
        filters.DjangoFilterBackend,
        jsonapi_filters.OrderingFilter,
    )
    search_fields = ("label",)
    ordering_fields = ("label", "balance")


class TransactionViewSet(views.ModelViewSet):
    """
    ViewSet для работы с моделью Transaction.

    Позволяет создавать, просматривать, обновлять и удалять транзакции.

    Поддерживает фильтрацию, сортировку и пагинацию.
    """

    queryset = Transaction.objects.select_related("wallet").all()
    serializer_class = TransactionSerializer
    pagination_class = PageNumberPagination
    filter_backends = (
        filters.DjangoFilterBackend,
        jsonapi_filters.OrderingFilter,
    )
    filter_fields = ("wallet",)
    search_fields = ("txid",)
    ordering_fields = ("txid", "amount")
