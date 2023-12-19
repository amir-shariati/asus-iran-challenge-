from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, ProductImage, ProductClass, ProductAttribute, OptionGroup, \
    OptionGroupValue, ProductAttributeValue


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent',)
    search_fields = ('title',)
    autocomplete_fields = ('parent',)
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 20


class ProductImageTabularInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    list_display = ('title', 'alt_text', )
    readonly_fields = ('img_preview',)

    @admin.display(description=_('image preview'))
    def img_preview(self, obj):
        return obj.img_preview()

    @admin.display(description=_('thumbnail image'))
    def thumbnail(self, obj):
        return obj.img_thumbnail()


class ProductAttributeTabularInline(admin.TabularInline):
    model = ProductAttribute
    extra = 0
    autocomplete_fields = ('option_group',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_per_page = 20


class ProductAttributeValueTabularInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    autocomplete_fields = ('attribute',)


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'require_shipping', 'track_stock', 'has_attributes', 'get_attribute_count'
    )
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title',)
    inlines = (
        ProductAttributeTabularInline,
    )

    list_per_page = 20

    @admin.display(description=_('attribute count'))
    def get_attribute_count(self, obj):
        return obj.attributes.count()


class OptionGroupValueTabularInline(admin.TabularInline):
    model = OptionGroupValue
    extra = 2


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    inlines = (
        OptionGroupValueTabularInline,
    )
    search_fields = ('title',)
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'inventory', 'price',
        'get_product_image'
    )

    autocomplete_fields = ('category', 'product_class')
    prepopulated_fields = {"slug": ("title",)}

    inlines = (
        ProductAttributeValueTabularInline,
        ProductImageTabularInline,
    )
    list_per_page = 20

    def get_queryset(self, obj):
        qs = super(ProductAdmin, self).get_queryset(obj)
        return qs.prefetch_related('product_images')

    @admin.display(description=_('image preview'))
    def get_product_image(self, obj):
        product_image_obj = obj.product_images.first()
        if product_image_obj is not None:
            return product_image_obj.img_preview()
        else:
            return None
