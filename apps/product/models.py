from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Category models
class Category(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Category title'))
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True)

    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='children',
                               verbose_name=_('Category parent')
                               )

    @property
    def is_last_child(self):
        """
        check whether current category is a parent for another category
        """
        return self.children.count() == 0

    @property
    def is_root_category(self):
        """
        Check whether current category has no parent
        """
        return self.parent is None

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        full_path = [self.slug]
        k = self.parent
        while k is not None:
            full_path.append(k.slug)
            k = k.parent
        slug_string = '/'.join(full_path[::-1])
        return reverse("product:product-detail", kwargs={"path": slug_string})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


# Product Image models
class ProductImage(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Product Image title'))
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_images")

    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Image alternative text"),
    )
    image = models.ImageField(
        upload_to='product_image/%Y/%m/%d/',
        verbose_name=_('Image'),
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(150, 150)],
        format='JPEG',
        options={'quality': 90},
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}"  width="150"/>')

    def img_thumbnail(self):
        return mark_safe(f'<img src = "{self.image.url}" width="64" />')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


# Option Group models
class OptionGroup(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Option Group title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Option Group')
        verbose_name_plural = _('Option Groups')


# Option Group Value  models
class OptionGroupValue(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Option Group Value title'))
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name='optionGroup_values')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Option Group Value')
        verbose_name_plural = _('Option Groups Value')


# Product Class models
class ProductClass(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name=_('Product class title'))
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('Product class description'))
    track_stock = models.BooleanField(default=True, verbose_name=_('Track Stock'))
    require_shipping = models.BooleanField(default=True, verbose_name=_('Require shipping'))

    @property
    def has_attributes(self):
        return self.attributes.exists()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product Class')
        verbose_name_plural = _('Product Classes')


# Product Attribute models
class ProductAttribute(models.Model):

    class AttributeTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, null=True, related_name='attributes')
    title = models.CharField(max_length=255, verbose_name=_('Product Attribute title'))
    type = models.CharField(max_length=16, choices=AttributeTypeChoice.choices, default=AttributeTypeChoice.text)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)
    required = models.BooleanField(default=False, verbose_name=_('Required'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product Attribute')
        verbose_name_plural = _('Product Attribute')


# Product Attribute Value models
class ProductAttributeValue(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value_text = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Value text'))
    value_integer = models.IntegerField(null=True, blank=True, verbose_name=_('Value integer'))
    value_float = models.FloatField(null=True, blank=True, verbose_name=_('Value float'))
    value_option = models.ForeignKey(
        OptionGroupValue,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='attribute_option_values',
        verbose_name=_('Value option')
    )
    value_multi_option = models.ManyToManyField(
        OptionGroupValue,
        null=True,
        blank=True,
        related_name='attribute_multi_option_values',
        verbose_name=_('Value multi option')
    )

    class Meta:
        verbose_name = _('Product Attribute Value')
        verbose_name_plural = _('Product Attribute Values')
        unique_together = ('product', 'attribute')


# Product models
class Product(models.Model):

    class ProductTypeChoice(models.TextChoices):
        standalone = 'standalone'
        parent = 'parent'
        child = 'child'

    structure = models.CharField(
        max_length=16,
        choices=ProductTypeChoice.choices,
        default=ProductTypeChoice.standalone,
        verbose_name=_('Product structure')
    )
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='children',
                               verbose_name=_('Product parent')
                               )

    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Product title'))
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True)

    upc = models.CharField(max_length=24, unique=True, null=True, blank=True, verbose_name=_('Product upc'))
    is_public = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=128, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    product_class = models.ForeignKey(
        ProductClass,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('Product class')
    )
    attributes = models.ManyToManyField(ProductAttribute, through=ProductAttributeValue)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Category'))

    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name=_('Price'))
    inventory = models.IntegerField(default=0, verbose_name=_('Inventory'))

    description = models.TextField(null=True, blank=True, verbose_name=_('Product description'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created time'))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_('Last update time'))

    @property
    def image_main(self):
        if self.product_images.exists():
            # return self.product_images.first()
            # return self.product_images.first().img_thumbnail()
            return self.product_images.first().img_preview()
        else:
            return None

    @property
    def is_last_product_child(self):
        """
        check whether current category is a parent for another category
        """
        return self.children.count() == 0

    @property
    def is_root_product(self):
        """
        Check whether current category has no parent
        """
        return self.parent is None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

