# Generated by Django 4.2.5 on 2023-10-04 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_optiongroup_productclass_alter_category_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='meta_title',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.product', verbose_name='Product parent'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.productclass', verbose_name='Product class'),
        ),
        migrations.AddField(
            model_name='product',
            name='structure',
            field=models.CharField(choices=[('standalone', 'Standalone'), ('parent', 'Parent'), ('child', 'Child')], default='standalone', max_length=16, verbose_name='Product structure'),
        ),
        migrations.AddField(
            model_name='product',
            name='upc',
            field=models.CharField(blank=True, max_length=24, null=True, unique=True, verbose_name='Product upc'),
        ),
        migrations.AlterField(
            model_name='optiongroup',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Option Group title'),
        ),
        migrations.AlterField(
            model_name='optiongroupvalue',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Option Group Value title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Product title'),
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_text', models.TextField(blank=True, null=True, verbose_name='Value title')),
                ('value_integer', models.IntegerField(blank=True, null=True, verbose_name='Value title')),
                ('value_float', models.FloatField(blank=True, null=True, verbose_name='Value title')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productattribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('value_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.optiongroupvalue', verbose_name='Value option')),
            ],
            options={
                'verbose_name': 'Product Attribute Value',
                'verbose_name_plural': 'Product Attribute Values',
                'unique_together': {('product', 'attribute')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(through='product.ProductAttributeValue', to='product.productattribute'),
        ),
    ]
