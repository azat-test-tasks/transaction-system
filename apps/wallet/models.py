"""Модуль для создания, настройки и управления моделями пакета `wallet`.

Models:
    Wallet:
        Основная модель приложения, через которую происходит взаимодействие с кошельком.
    Transaction:
        Модель для хранения транзакций кошелька.
"""

from django.db import models


class Wallet(models.Model):
    """Модель для кошелька.

    Основная модель приложения, через которую происходит взаимодействие с кошельком.

    Attributes:
        label(str):
            Название кошелька. Установлены ограничения по длине.
        balance(int):
            Баланс кошелька. Установлены ограничения по длине.
    """

    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    class Meta:
        db_table = "wallet"
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.label} - {self.balance}"


class Transaction(models.Model):
    """Транзакция кошелька.

    Модель связывает Wallet и Transaction. Позволяет хранить информацию о транзакциях кошелька.

    Attributes:
        wallet(int):
            Связанный кошелек. Связь через ForeignKey.
        txid(str):
            Обязательный уникальный строковой идентификатор транзакции.
        amount(int):
            Количество средств, которые были переведены на кошелек.
    """

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = "transaction"
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=["txid"]),
        ]

    def __str__(self):
        return f"{self.wallet.label} - {self.txid}"
