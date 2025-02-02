from rest_framework.routers import DefaultRouter

from app.customerorders.views import (
    CustomerViewSet,
    OrdersViewSet,
)

router = DefaultRouter()


router.register(r"customers", CustomerViewSet, "customers")
router.register(r"orders", OrdersViewSet, "orders")


urlpatterns = []


urlpatterns += router.urls
