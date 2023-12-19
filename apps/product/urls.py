from django.urls import path, include
from .views import ProductListView, ProductDetailView


app_name = "product"

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<path:path>', ProductDetailView.as_view(), name='product-detail'),
]
