from rest_framework import routers

from apps.wallet.views import TransactionViewSet, WalletViewSet


router = routers.DefaultRouter()
router.register(r"transactions", TransactionViewSet)
router.register(r"wallets", WalletViewSet)

urlpatterns = router.urls
