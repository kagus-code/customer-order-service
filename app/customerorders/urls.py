from rest_framework.routers import DefaultRouter

from app.customerorders.views import (
    CustomerViewSet,
    OrdersViewSet,
)

router = DefaultRouter()


router.register(r"orders", OrdersViewSet, "orders")
router.register(r"", CustomerViewSet, "customers")


urlpatterns = []


urlpatterns += router.urls
