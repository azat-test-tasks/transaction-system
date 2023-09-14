import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.wallet.models import Transaction


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    """
    Этот сигнал обновляет баланс кошелька после создания новой транзакции.

    :param sender: Класс модели, который отправил сигнал (Transaction).
    :param instance: Экземпляр транзакции, которая была создана.
    :param created: Флаг, указывающий, была ли создана новая транзакция.
    :param kwargs: Дополнительные аргументы.
    """
    if created:
        wallet = instance.wallet
        wallet.balance += instance.amount
        wallet.save()
        logger.info(
            f"Balance updated for wallet: {wallet.label}. New balance: {wallet.balance}"
        )
