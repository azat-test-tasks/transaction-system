from rest_framework import serializers

from apps.wallet.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Wallet.

    Поля:
    - id (автоматический)
    - label (строковое поле)
    - balance (сумма всех сумм транзакций)
    """

    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Transaction.

    Поля:
    - id (автоматический)
    - wallet (внешний ключ к модели Wallet)
    - txid (уникальное строковое поле)
    - amount (число с точностью до 18 знаков после запятой)
    """

    class Meta:
        model = Transaction
        fields = "__all__"
