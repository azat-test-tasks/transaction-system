import decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.wallet.models import Transaction, Wallet
from apps.wallet.serializers import TransactionSerializer


class TransactionAPITestCase(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(
            label="Test Wallet", balance=1000.00
        )
        self.transaction_data = {
            "wallet": self.wallet.id,
            "txid": "test_txid",
            "amount": decimal.Decimal("100.50"),
        }
        self.transaction_serializer = TransactionSerializer(
            data=self.transaction_data
        )

    def test_create_transaction(self):
        """
        Тест создания транзакции и проверки обновления баланса кошелька.
        """
        response = self.client.post(
            reverse("transaction-list"), self.transaction_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

        # Получить кошелек заново из базы данных, чтобы убедиться, что баланс обновился.
        self.wallet.refresh_from_db()

        # Проверяем, что баланс кошелька обновился
        self.assertEqual(self.wallet.balance, decimal.Decimal("1100.50"))

    def test_list_transactions(self):
        """
        Тест получения списка всех транзакций.
        """
        wallet = Wallet.objects.create(
            label="Test Wallet", balance=decimal.Decimal("2000.00")
        )

        # Создаем несколько транзакций
        transaction_data_1 = {
            "wallet": wallet,
            "txid": "txid_1",
            "amount": decimal.Decimal("50.25"),
        }
        transaction_data_2 = {
            "wallet": wallet,
            "txid": "txid_2",
            "amount": decimal.Decimal("75.75"),
        }
        Transaction.objects.create(**transaction_data_1)
        Transaction.objects.create(**transaction_data_2)

        # Получаем список всех транзакций
        url = reverse("transaction-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_transactions(self):
        """
        Тест фильтрации транзакций по txid.
        """
        # Создаем новый кошелек
        wallet = Wallet.objects.create(
            label="Test Wallet", balance=decimal.Decimal("1000.00")
        )

        # Создаем несколько транзакций, привязанных к этому кошельку
        transaction_data_1 = {
            "wallet": wallet,
            "txid": "txid_1",
            "amount": decimal.Decimal("50.25"),
        }
        transaction_data_2 = {
            "wallet": wallet,
            "txid": "txid_2",
            "amount": decimal.Decimal("75.75"),
        }
        Transaction.objects.create(**transaction_data_1)
        Transaction.objects.create(**transaction_data_2)

        # Фильтруем транзакции по txid
        response = self.client.get(
            reverse("transaction-list"), {"txid": "txid_1"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["txid"], "txid_1")


class WalletAPITestCase(APITestCase):
    def test_create_wallet(self):
        """
        Тест создания нового кошелька.
        """
        wallet_data = {
            "label": "New Wallet",
        }
        response = self.client.post(
            reverse("wallet-list"), wallet_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)
