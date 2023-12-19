from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product, Category, ProductImage


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        qs = qs.select_related('category').prefetch_related('product_images').order_by("-id")
        return qs


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        path = self.kwargs.get('path')
        slug = path.split('/')[-1]
        product = Product.objects.select_related('category').get(slug=slug)
        return product

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the image
        context["image_obj"] = self.get_object().product_images.all()
        return context
