from django.contrib import admin

from apps.wallet.models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "balance")
    search_fields = ("label",)
    ordering = ("-id",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "txid", "wallet", "amount")
    list_filter = ("wallet",)
    search_fields = ("txid", "wallet__label")
    ordering = ("-id",)
