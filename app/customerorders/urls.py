from rest_framework.routers import DefaultRouter

from app.customerorders.views import CustomerViewSet

router = DefaultRouter()


router.register(r"customer", CustomerViewSet, "customer")


urlpatterns = []


urlpatterns += router.urls
